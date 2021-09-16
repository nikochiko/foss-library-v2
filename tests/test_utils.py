from fosslib.utils import (
    convert_isbn10_to_isbn13,
    convert_isbn13_to_isbn10,
    get_book_cover_by_isbn,
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


def test_cover_image_from_isbn():
    isbn = "9780007220854"

    cover_image = get_book_cover_by_isbn(isbn)
    assert cover_image == "https://covers.openlibrary.org/b/id/4935512-M.jpg"
