"""Admin blueprint."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, user_passes_test
from app import db
from app.models import User
from app.forms import UserForm

admin_bp = Blueprint("admin", __name__)


def admin_only(user):
    return user.is_admin


@admin_bp.route("/")
@login_required
@user_passes_test(admin_only)
def index():
    """List all users."""
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/create", methods=["GET", "POST"])
@login_required
@user_passes_test(admin_only)
def create():
    """Create a new user."""
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("admin.create"))
        user = User(
            username=form.username.data,
            full_name=form.full_name.data,
            email=form.email.data,
            is_admin=form.is_admin.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User created successfully.", "success")
        return redirect(url_for("admin.index"))
    return render_template("admin/user_form.html", form=form)


@admin_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@user_passes_test(admin_only)
def edit(user_id):
    """Edit a user."""
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("User updated successfully.", "success")
        return redirect(url_for("admin.index"))
    return render_template("admin/user_form.html", form=form)


@admin_bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
@user_passes_test(admin_only)
def delete(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "info")
    return redirect(url_for("admin.index"))
