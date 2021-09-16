from fosslib.database import CRUDMixin, db


class Book(db.Model, CRUDMixin):
    """The Book model"""

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn10 = db.Column(db.String(10), unique=True, nullable=False, index=True)
    isbn13 = db.Column(db.String(13), unique=True, nullable=False, index=True)

    cover_image = db.Column(db.String(255))

    # the longest book title is over 26000 characters! won't use VARCHAR(X) here
    title = db.Column(db.Text)
    authors = db.Column(db.Text)

    # langauge code is usually 3 chars long, but there is a special code qaa-qtz
    language_code = db.Column(db.String(7), index=True)
    num_pages = db.Column(db.Integer)

    average_rating = db.Column(db.Float)
    ratings_count = db.Column(db.Integer)
    text_reviews_count = db.Column(db.Integer)

    publication_date = db.Column(db.DateTime)
    publisher_name = db.Column(db.String(255))

    total_stock = db.Column(db.Integer, default=1)

    # default rent per day to 1 Rs per day
    rent_per_day = db.Column(db.Integer, default=10)

    # timestamps
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    title_text_pattern_idx = db.Index(
        f"idx_{__tablename__}_title_lower_text_pattern",
        db.func.lower(title).label("lowercase_title"),
        postgresql_ops={"lowercase_title": "text_pattern_ops"},
    )
    authors_text_pattern_idx = db.Index(
        f"idx_{__tablename__}_authors_lower_text_pattern",
        db.func.lower(title).label("lowercase_authors"),
        postgresql_ops={"lowercase_authors": "text_pattern_ops"},
    )
    publisher_name_varchar_pattern_idx = db.Index(
        f"idx_{__tablename__}_publisher_lower_text_pattern",
        db.func.lower(title).label("lowercase_publisher_name"),
        postgresql_ops={"lowercase_publisher_name": "varchar_pattern_ops"},
    )

    @property
    def unreturned_stock(self):
        """Number of unreturned books"""
        unreturned_books = Issuals.query.filter_by(
            book_id=self.id, returned_at=None
        ).count()
        return unreturned_books

    @property
    def available_stock(self):
        """Returns the available stock for a Book"""
        return self.total_stock - self.unreturned_stock
