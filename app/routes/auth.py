"""Authentication blueprint."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms_dir.login_form import LoginForm
from app.forms_dir.register_form import RegisterForm
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))
        user = User(
            username=form.username.data,
            full_name=form.full_name.data,
            email=form.email.data,
            is_admin=form.is_admin.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully, you can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


# Password reset routes
@auth_bp.route("/password-reset", methods=["GET", "POST"])
def password_reset_request():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("No account with that email.", "danger")
            return redirect(url_for("auth.password_reset_request"))
        # Generate token
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = serializer.dumps(user.id, salt="password-reset", expires_in=3600)
        # Store token and expiration
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        reset_url = url_for("auth.password_reset", token=token)
        flash("Password reset link sent.", "success")
        return redirect(reset_url)
    return render_template("password_reset_request.html", form=form)


@auth_bp.route("/password-reset/<token>")
def password_reset(token):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        user_id = serializer.loads(token, salt="password-reset", max_age=3600)
    except (BadSignature, SignatureExpired):
        flash("Invalid or expired reset link.", "danger")
        return redirect(url_for("auth.password_reset_request"))
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.password_reset_request"))
    if request.method == "POST":
        new_password = request.form.get("new_password")
        if new_password:
            user.set_password(new_password)
            user.password_reset_token = None
            user.password_reset_expires = None
            db.session.commit()
            flash("Password updated successfully.", "success")
            return redirect(url_for("auth.login"))
        # else fall through to render template
    return render_template("password_reset.html", user=user)
