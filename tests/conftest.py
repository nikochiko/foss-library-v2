import pytest
from testing.postgresql import Postgresql

from fosslib.app import create_app, db


@pytest.fixture
def app():
    with Postgresql() as postgres:
        db_url = postgres.url()

        app = create_app(
            "tests.settings",
            overrides={"SQLALCHEMY_DATABASE_URI": db_url},
        )

        with app.app_context():
            db.create_all()

        yield app


@pytest.fixture
def client(app):
    return app.test_client()
