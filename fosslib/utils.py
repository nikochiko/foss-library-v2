import hashlib
from math import ceil
from contextlib import contextmanager
from urllib.parse import urlencode

import aiohttp
from flask import abort, flash, request


class PaginationError(Exception):
    pass


class Pagination:
    default_page = 1
    default_per_page = 20
    default_max_per_page = 50

    def __init__(
        self,
        query,
        page=None,
        per_page=None,
        max_per_page=None,
    ):
        # the query object without a SQL limit applied
        self.query = query

        # current page number
        self.page = page
        # items to displayed on each page
        self.per_page = per_page
        # max value of self.per_page (used for validation)
        self.max_per_page = max_per_page or self.__class__.default_max_per_page

        self.init_from_request_args()

        # validate page, per_page before doing a DB query
        self.validate_pagination_args()

        self.total = self.get_total()
        self.items = self.get_items()
        self.total_pages = self.get_total_pages()

    def init_from_request_args(self):
        if self.page is None:
            with try_or_abort(PaginationError, 404):
                self.page = self.get_int_param_from_request(
                    "page", self.__class__.default_page
                )

        if self.per_page is None:
            with try_or_abort(PaginationError, 404):
                self.per_page = self.get_int_param_from_request(
                    "per_page",
                    self.__class__.default_per_page,
                )

    def validate_pagination_args(self):
        with try_or_abort(AssertionError, 404):
            self.validate_page()
            self.validate_per_page()

    def validate_per_page(self):
        assert self.per_page > 0, "There should be at least 1 item per page"
        assert (
            self.per_page <= self.max_per_page
        ), f"There cannot be more than {self.max_per_page} items on each page"

    def validate_page(self):
        assert self.page >= 1, "Page should be at least 1"

    def get_total(self):
        return self.query.count()

    def get_items(self):
        limit = self.per_page
        offset = self.per_page * (self.page - 1)
        return self.query.offset(offset).limit(limit).all()

    def get_total_pages(self):
        return ceil(self.total / self.per_page)

    def get_int_param_from_request(self, param, default):
        value = request.args.get(param, default)
        try:
            value = int(value)
        except (ValueError, TypeError):
            # this error is probably because the query param wasn't an int
            raise PaginationError(f"Couldn't convert {param} arg to int")

        return value


@contextmanager
def try_or_abort(exc_classes, abort_code):
    try:
        yield
    except exc_classes:
        abort(abort_code)


def convert_isbn10_to_isbn13(isbn10: str) -> str:
    """
    Utility function for converting an ISBN-10 code to an ISBN-13 code

    https://isbn-information.com/convert-isbn-10-to-isbn-13.html
    """
    assert len(isbn10) == 10, "ISBN-10 must be a 10-digit string"

    partial_isbn13 = "978" + isbn10[:9]

    check_digit = get_check_digit_for_isbn13(partial_isbn13)

    isbn13 = partial_isbn13 + check_digit

    return isbn13


def convert_isbn13_to_isbn10(isbn13: str) -> str:
    """
    Utility function for converting an ISBN-13 code to an ISBN-10 code
    """
    assert len(isbn13) == 13, "ISBN-13 must be a 13-digit string"
    assert isbn13.startswith("978"), "ISBN-13 must start with Bookland 978"

    partial_isbn10 = isbn13[3:12]

    check_digit = get_check_digit_for_isbn10(partial_isbn10)

    isbn10 = partial_isbn10 + check_digit

    return isbn10


def get_check_digit_for_isbn13(partial_isbn13: str) -> str:
    """
    Gets the check digit for an incomplete ISBN-13 code

    This check digit is the last digit of an ISBN code
    """
    sum_ = 0
    multiply_3 = False

    for ch in partial_isbn13[:12]:
        to_add = int(ch)

        if multiply_3:
            to_add *= 3

        sum_ += to_add

        # we need to multiply with 3 alternately, hence toggling this bool
        multiply_3 = not multiply_3

    intermediate_digit = sum_ % 10
    check_digit = (10 - intermediate_digit) % 10

    check_digit = str(check_digit)

    return check_digit


def get_check_digit_for_isbn10(partial_isbn10: str) -> str:
    """
    Gets the check digit for an incomplete ISBN-10 code

    This check digit is the last digit of an ISBN code
    """
    sum_ = 0
    multiplier = 10

    for ch in partial_isbn10[:9]:
        sum_ += int(ch) * multiplier

        multiplier -= 1

    intermediate_digit = sum_ % 11
    check_digit = (11 - intermediate_digit) % 11

    if check_digit == 10:
        check_digit = "X"
    else:
        check_digit = str(check_digit)

    return check_digit


async def get_cover_image_by_isbn(session: aiohttp.ClientSession, isbn: str) -> str:
    """Returns the book cover for the given book using OpenLibrary API"""
    cover_id = await get_cover_id_by_isbn(session, isbn)

    if cover_id is None:
        return None

    cover_image_url = get_cover_image_by_cover_id(cover_id)

    return cover_image_url


async def get_cover_id_by_isbn(session: aiohttp.ClientSession, isbn: str) -> int:
    """Gets the book cover ID from OpenLibrary API"""
    isbn_api_url = f"https://openlibrary.org/isbn/{isbn}.json"

    async with session.get(isbn_api_url) as response:
        response.raise_for_status()
        response_data = await response.json()

    if "covers" not in response_data:
        return None

    return response_data["covers"][0]


def get_cover_image_by_cover_id(cover_id: int) -> str:
    """Gets the cover image URL from cover id"""
    cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    return cover_image_url


def flash_form_errors(form, category="warning"):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def get_gravatar_image_url(email: str) -> str:
    """Gets the gravatar image URL for an email"""
    gravatar_base_url = "https://www.gravatar.com/avatar"

    default = "https://upload.wikimedia.org/wikipedia/commons/1/1e/Default-avatar.jpg"
    size = 40

    email_hash = hashlib.md5(email.lower().encode()).hexdigest()
    query_params = urlencode({"d": default, "s": str(size)})

    url = f"{gravatar_base_url}/{email_hash}?{query_params}"

    return url
