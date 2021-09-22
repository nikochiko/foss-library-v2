from fosslib.members.models import Member
from .utils import _test_url_for_GET_request

URLs = {
    "list": "/members/",
    "create": "/members/create/"
}


valid_member_payload = {
    "first_name": "test",
    "last_name": "testlast",
    "email": "somethingunique@example.com",
}

invalid_member_payload = {
    "first_name": "test",
    "last_name": "testlast",
    "email": "invalidemail",
}


def test_list_members_view(client):
    url = URLs["list"]

    _test_url_for_GET_request(client, url)


def test_create_members_view_with_GET_method(client):
    url = URLs["create"]

    _test_url_for_GET_request(client, url)


def test_create_members_view_when_adding_valid_member(app, client):
    url = URLs["create"]
    payload = valid_member_payload

    response = client.post(url, data=payload)

    assert response.status_code == 200

    with app.app_context():
        assert Member.query.count() == 1
        assert Member.query.first().email == valid_member_payload["email"]


def test_create_members_view_when_adding_invalid_member(app, client):
    url = URLs["create"]
    payload = invalid_member_payload

    response = client.post(url, data=payload)

    # 200 response because we are showing HTML for the form again
    assert response.status_code == 200

    with app.app_context():
        # assert that invalid member hasn't been added to DB
        assert Member.query.count() == 0
