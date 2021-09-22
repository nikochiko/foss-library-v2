import aiohttp
import pytest

from fosslib.utils import (
    convert_isbn10_to_isbn13,
    convert_isbn13_to_isbn10,
    get_cover_image_by_isbn,
    get_gravatar_image_url,
)


def test_isbn10_to_isbn13():
    # test case 1
    isbn10 = "0345391802"
    isbn13 = "9780345391803"

    assert convert_isbn10_to_isbn13(isbn10) == isbn13

    # test case 2
    isbn10 = "0061122416"
    isbn13 = "9780061122415"

    assert convert_isbn10_to_isbn13(isbn10) == isbn13


def test_isbn13_to_isbn10():
    # test case 1
    isbn13 = "9780007220854"
    isbn10 = "0007220855"

    assert convert_isbn13_to_isbn10(isbn13) == isbn10

    # test case 2
    isbn13 = "9781449340377"
    isbn10 = "1449340377"

    assert convert_isbn13_to_isbn10(isbn13) == isbn10


@pytest.mark.asyncio
async def test_cover_image_from_isbn():
    isbn = "9780007220854"

    async with aiohttp.ClientSession() as session:
        cover_image = await get_cover_image_by_isbn(session, isbn)

    assert cover_image == "https://covers.openlibrary.org/b/id/4935512-M.jpg"


def test_get_gravatar_image_url():
    # for now, just test that it doesn't raise an error
    email = "test@example.com"

    try:
        get_gravatar_image_url(email)
    except Exception as e:
        pytest.fail(str(e))
