def _test_url_for_GET_request(client, url):
    """Sends a GET request to the URL and asserts that status code was 200"""

    response = client.get(url)

    assert response.status_code == 200, f"GET {url} should return 200 response"
