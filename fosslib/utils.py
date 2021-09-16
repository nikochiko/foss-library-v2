import requests


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


def get_book_cover_by_isbn(isbn: str) -> str:
    """Returns the book cover for the given book using OpenLibrary API"""
    cover_id = get_cover_id_by_isbn(isbn)
    cover_image_url = get_cover_image_from_cover_id(cover_id)

    return cover_image_url


def get_cover_id_by_isbn(isbn: str) -> int:
    """Gets the book cover ID from OpenLibrary API"""
    isbn_api_url = f"https://openlibrary.org/isbn/{isbn}.json"

    r = requests.get(isbn_api_url)
    r.raise_for_status()

    response_data = r.json()
    return response_data["covers"][0]


def get_cover_image_from_cover_id(cover_id: int) -> str:
    """Gets the cover image URL from cover id"""
    cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    return cover_image_url
