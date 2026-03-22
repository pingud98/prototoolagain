"""SQLAlchemy models for the Inspection Reporting and Management app."""

from datetime import datetime
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import bcrypt

from app import db


class User(db.Model, UserMixin):
    """User account for authentication and authorization."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
     created_at = db.Column(db.DateTime, default=datetime.utcnow)
      # Password reset fields
     password_reset_token = db.Column(db.String(64), nullable=True)
     password_reset_expires = db.Column(db.DateTime, nullable=True)

    # Password handling
    def set_password(self, password: str) -> None:
        """Hash and store a password."""
        self.password_hash = bcrypt.hash(password, rounds=12)

    def check_password(self, password: str) -> bool:
        """Check a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)


class Inspection(db.Model):
    """A single inspection report."""

    id = db.Column(db.Integer, primary_key=True)
    installation_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    inspection_date = db.Column(db.Date, nullable=False)
    version = db.Column(db.Integer, nullable=False, default=1)
    reference_number = db.Column(db.Integer, nullable=False)
    observations = db.Column(db.Text, nullable=True)
    conclusion_text = db.Column(db.Text, nullable=True)
    conclusion_status = db.Column(
        db.String(20), nullable=False, default="ok"
    )  # ok / minor / major
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    creator = db.relationship("User", backref="inspections")
    inspectors = db.relationship(
        "InspectionInspector", backref="inspection", cascade="all, delete-orphan"
    )
    photos = db.relationship(
        "Photo", backref="inspection", cascade="all, delete-orphan"
    )


class InspectionInspector(db.Model):
    """Inspector for an inspection – either a registered user or a free‑text name."""

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(
        db.Integer, db.ForeignKey("inspection.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    free_text_name = db.Column(db.String(120), nullable=True)

    __unique__ = ("inspection_id", "user_id")


class Photo(db.Model):
    """Photo attached to an inspection."""

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(
        db.Integer, db.ForeignKey("inspection.id"), nullable=False
    )
    filename = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200), nullable=True)
    action_required = db.Column(
        db.String(20), nullable=False, default="none"
    )  # none / urgent / before_next
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
