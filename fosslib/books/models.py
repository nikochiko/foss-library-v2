from datetime import date, datetime

from pony import orm

from fosslib.database import db


class Book(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    isbn10 = orm.Required(str)
    isbn13 = orm.Required(str)
    cover_image = orm.Required(
        str,
        default="https://upload.wikimedia.org/wikipedia/commons/7/72/Placeholder_book.svg",
    )
    publisher = orm.Required(str)
    publication_date = orm.Required(date)
    language_code = orm.Required(str)
    authors = orm.Required(str)
    frappe_id = orm.Optional(int)

    created_at = orm.Required(datetime, default=datetime.utcnow)
    updated_at = orm.Required(datetime, default=datetime.utcnow)
