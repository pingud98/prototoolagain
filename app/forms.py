"""WTForms for the application."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=64)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired()]
    )
    submit = SubmitField("Login")