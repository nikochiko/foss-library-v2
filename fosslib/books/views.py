from flask import Blueprint, render_template, request

from fosslib.utils import Pagination
from .models import Book

blueprint = Blueprint("books", __name__, url_prefix="/books")


@blueprint.route("/", methods=("GET",))
def list():
    query = get_book_query_from_request_args()
    pagination = Pagination(query)

    return render_template("books/list.html", pagination=pagination)


@blueprint.route("/<int:id>/", methods=("GET",))
def show(id):
    book = Book.query.get_or_404(id)

    return render_template("books/show.html", book=book)


def get_book_query_from_request_args():
    query = Book.query

    if "q" in request.args:
        search_term = request.args.get("q")
        sql_like_arg = f"%{search_term}%"
        query = query.filter(
            Book.title.ilike(sql_like_arg)
            | Book.authors.ilike(sql_like_arg)
            | Book.publisher_name.ilike(sql_like_arg)
            | Book.isbn13.ilike(sql_like_arg)
        )

    return query
