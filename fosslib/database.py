from flask import current_app
from pony.orm import Database


def initialise_pony_db():
    db = Database()

    # only initialising if we are in app context
    if current_app:
        db.bind(**current_app.config["PONY"])

    return db


db = initialise_pony_db()
