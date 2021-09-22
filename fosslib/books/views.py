from flask import Blueprint, flash, redirect, render_template, request, url_for

from fosslib.exceptions import FOSSLibBaseException
from fosslib.utils import Pagination
from fosslib.members.models import Member
from .models import Book

blueprint = Blueprint("books", __name__, url_prefix="/books")


@blueprint.route("/", methods=("GET",))
def list():
    query = get_book_query_from_request_args()
    pagination = Pagination(query)

    return render_template("books/list.html", pagination=pagination)


@blueprint.route("/show/<int:id>/", methods=("GET",))
def show(id):
    book = Book.query.get_or_404(id)

    return render_template("books/show.html", book=book)


@blueprint.route("/delete/<int:id>/", methods=("GET",))
def delete(id):
    book = Book.query.get_or_404(id)

    book.delete()

    flash("Book deleted successfully", "success")
    return redirect(url_for('books.list'))


@blueprint.route("/issue/<int:book_id>/to/<int:member_id>", methods=("POST",))
def issue(book_id, member_id):
    book = Book.query.get_or_404(book_id)
    member = Member.query.get_or_404(member_id)

    try:
        book.issue_to(member)
        flash("Book issued successfully!", "success")
    except FOSSLibBaseException as e:
        flash(str(e), "warning")

    return redirect(url_for("books.show", id=book_id))


@blueprint.route("/update/<int:id>/", methods=("GET", "POST"))
def update(id):
    pass


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
