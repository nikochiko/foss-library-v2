from flask import Blueprint, flash, render_template
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


@blueprint.route("/create/", methods=("GET", "POST"))
def create():
    template_path = "members/create.html"

    form = MemberForm()
    if form.validate_on_submit():
        member = Member()
        form.populate_obj(member)

        member.gravatar_url = get_gravatar_image_url(member.email)

        # may be room for improvement here. return
        # a friendlier error than one thrown by DB
        try:
            member.save()
        except IntegrityError as e:
            flash(e, "danger")
            return render_template(template_path)

    flash_form_errors(form)
    return render_template(template_path)


def get_member_query_from_request_args():
    query = Member.query

    # TODO: add support for search terms

    return query
