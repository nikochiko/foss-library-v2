from flask import Blueprint, current_app, flash, render_template
from sqlalchemy.exc import IntegrityError

from fosslib.utils import Pagination, flash_form_errors, get_gravatar_image_url
from .forms import MemberForm
from .models import Member


blueprint = Blueprint("members", __name__, url_prefix="/members")


@blueprint.route("/", methods=("GET",))
def list():
    template_path = "members/list.html"

    query = get_member_query_from_request_args()
    pagination = Pagination(query)

    return render_template(template_path, pagination=pagination)


@blueprint.route("/show/", methods=("GET",))
def show():
    template_path = "members/show.html"

    return render_template("layout.html")


@blueprint.route("/create/", methods=("GET", "POST"))
def create():
    template_path = "members/create.html"

    form = MemberForm()
    if form.validate_on_submit():
        member = Member()
        form.populate_obj(member)

        member.gravatar_url = get_gravatar_image_url(member.email)

        # some room for improvemen with error handling here
        try:
            member.save()
            flash("Member added!", "success")
        except IntegrityError as e:
            current_app.logger.info(f"IntegrityError: {e}")
            flash(
                "There was some error while trying to add the "
                "new member. Maybe the email is already in use?",
                "danger"
            )
            return render_template(template_path, form=form)

    flash_form_errors(form)
    return render_template(template_path, form=form)


def get_member_query_from_request_args():
    query = Member.query

    # TODO: add support for search terms

    return query
