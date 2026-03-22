"""WTForms for the application."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    DateField,
    TextAreaField,
    SelectField,
    FileField,
    BooleanField,
    RadioField,
)
import os
from werkzeug.utils import secure_filename

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError,
)

from flask_login import current_user


def validate_unique_username(username):
    from app.models import User

    if User.query.filter_by(username=username).first():
        raise ValidationError("Username already taken.")


def validate_unique_email(email):
    from app.models import User

    if User.query.filter_by(email=email).first():
        raise ValidationError("Email already registered.")


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=64)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UserForm(FlaskForm):
    """User creation and edit form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=64)]
    )
    full_name = StringField(
        "Full Name", validators=[DataRequired(), Length(min=1, max=120)]
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password")
    is_admin = BooleanField("Admin")
    submit = SubmitField("Submit")

    def validate_username(self, field):
        if current_user and current_user.id != field.data:
            validate_unique_username(field.data)

    def validate_email(self, field):
        if current_user and current_user.id != field.data:
            validate_unique_email(field.data)


class InspectionForm(FlaskForm):
    def validate_photo_upload(form, field):
        from wtforms.validators import ValidationError
    
        allowed_extensions = {"jpg", "jpeg", "png", "gif", "webp"}
        max_size_mb = 10
        for file in field.data:
            if file:
                ext = file.filename.rsplit(".", 1)[-1].lower()
                if ext not in allowed_extensions:
                    raise ValidationError(
                        "Invalid file type. Allowed types: jpg, jpeg, png, gif, webp."
                    )
                # Check file size
                file.seek(0, 2)  # seek to end
                size = file.tell()
                file.seek(0)  # reset to start
                if size > max_size_mb * 1024 * 1024:  # 10MB in bytes
                    raise ValidationError("File size must be <= 10MB.")
    """Inspection report form."""

    installation_name = StringField(
        "Installation Name", validators=[DataRequired(), Length(max=120)]
    )
    location = StringField("Location", validators=[DataRequired(), Length(max=120)])
    inspection_date = DateField("Date of Inspection", validators=[DataRequired()])
    reference_number = IntegerField("Reference Number", validators=[DataRequired()])
    observations = TextAreaField("Observations", validators=[DataRequired()])
    conclusion_text = TextAreaField("Conclusion Comments", validators=[DataRequired()])
    conclusion_status = RadioField(
        "Conclusion Status",
        choices=[
            ("ok", "OK for operation in current state"),
            (
                "minor",
                "Minor comments — Remedial actions required for continued operation",
            ),
            (
                "major",
                "Major comments — Operation suspended until resolution and satisfactory follow-up inspection",
            ),
        ],
        default="ok",
    )
    # Inspectors (multiple) as a field of selectable users and free-text names
    inspectors = SelectField("Inspectors", coerce=int, validators=[DataRequired()])
    # Photo upload field
    photos = FileField(
        "Photos", validators=[DataRequired(), validate_photo_upload], multiple=True
    )
    submit = SubmitField("Complete Report")


class PhotoForm(FlaskForm):
    """Photo upload form."""

    caption = StringField("Caption", validators=[Length(max=255)])
    action_required = RadioField(
        "Action Required",
        choices=[
            ("none", "No action required"),
            ("urgent", "Urgent action required"),
            ("before_next", "Action required before next inspection"),
        ],
        default="none",
    )
    submit = SubmitField("Upload")


