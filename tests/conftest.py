import os

import pytest
from testing.postgresql import Postgresql

from fosslib.app import create_app, db


@pytest.fixture
def app():
    if os.getenv("TEST_ENV") == "CIRCLECI":
        # on circleci, a database container is used
        # we should take the DB config from there
        db_url = os.getenv("DATABASE_URL")
    else:
        # locally, we should create a new database for local testing
        _postgres_db = Postgresql()
        db_url = _postgres_db.url()

    try:
        app = create_app(
            "tests.settings",
            overrides={"SQLALCHEMY_DATABASE_URI": db_url}
        )

        with app.app_context():
            db.create_all()

        yield app

    finally:
        if os.getenv("TEST_ENV") != "CIRCLECI":
            _postgres_db.stop()


@pytest.fixture
def client(app):
    return app.test_client()
