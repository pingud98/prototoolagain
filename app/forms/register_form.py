"""Registration form for user creation."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Boolean
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Email()])
    full_name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    is_admin = BooleanField("Admin")
    submit = SubmitField("Register")
