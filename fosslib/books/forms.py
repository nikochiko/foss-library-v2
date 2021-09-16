from flask_wtf import FlaskForm
from wtforms.fields.html5 import SearchField


class SearchBookForm(FlaskForm):
    term = SearchField()
    title = SearchField()
    author = SearchField()
    publisher = SearchField()
