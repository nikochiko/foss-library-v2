from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired


class MemberForm(FlaskForm):
    first_name = StringField(validators=[InputRequired()])
    last_name = StringField(validators=[InputRequired()])
    email = EmailField(validators=[InputRequired(), Email()])
