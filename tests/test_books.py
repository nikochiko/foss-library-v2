URLs = {
    "list": "/books/",
}


def test_list_books_view(client):
    url = URLs["list"]

    response = client.get(url)

    assert response.status_code == 200, "GET list books should return 200 response"
