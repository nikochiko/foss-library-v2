from fosslib.database import CRUDMixin, db


class Member(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    gravatar_url = db.Column(db.String)
    dues_paid = db.Column(db.Integer, default=0)
