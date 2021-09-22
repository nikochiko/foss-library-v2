from .utils import _test_url_for_GET_request

URLs = {
    "list": "/books/",
}


def test_list_books_view(client):
    url = URLs["list"]

    _test_url_for_GET_request(client, url)
