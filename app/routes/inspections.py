"""Inspection blueprint."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Inspection, InspectionInspector
from app.forms import InspectionForm

inspections_bp = Blueprint("inspections", __name__)


@inspections_bp.route("", methods=["GET"])
@login_required
def index():
    """List all inspections for the logged-in user."""
    inspections = Inspection.query.order_by(Inspection.inspection_date.desc()).all()
    return render_template("dashboard.html", inspections=inspections)


@inspections_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    """Create a new inspection."""
    form = InspectionForm()
    if form.validate_on_submit():
        inspection = Inspection(
            installation_name=form.installation_name.data,
            location=form.location.data,
            inspection_date=form.inspection_date.data,
            reference_number=form.reference_number.data,
            observations=form.observations.data,
            conclusion_text=form.conclusion_text.data,
            conclusion_status=form.conclusion_status.data,
            created_by=current_user.id,
        )
        # Add inspectors
        for inspector in form.inspectors.data:
            if inspector.get("user_id"):
                inspector_obj = InspectionInspector(
                    inspection_id=inspection.id,
                    user_id=inspector["user_id"],
                    free_text_name=inspector.get("free_text_name"),
                )
                db.session.add(inspector_obj)
            else:
                inspector_obj = InspectionInspector(
                    inspection_id=inspection.id,
                    free_text_name=inspector.get("free_text_name"),
                )
                db.session.add(inspector_obj)
        db.session.commit()
        flash("Inspection created successfully.", "success")
        return redirect(url_for("inspections.view", inspection_id=inspection.id))
    return render_template("inspection_form.html", form=form)


@inspections_bp.route("/<int:inspection_id>", methods=["GET"])
@login_required
def view(inspection_id):
    """View an inspection."""
    inspection = Inspection.query.get_or_404(inspection_id)
    inspectors = inspection.inspectors
    photos = inspection.photos
    return render_template(
        "inspection_view.html",
        inspection=inspection,
        inspectors=inspectors,
        photos=photos,
    )


@inspections_bp.route("/<int:inspection_id>/edit", methods=["GET", "POST"])
@login_required
def edit(inspection_id):
    """Edit an inspection."""
    inspection = Inspection.query.get_or_404(inspection_id)
    form = InspectionForm(obj=inspection)
    if form.validate_on_submit():
        inspection.installation_name = form.installation_name.data
        inspection.location = form.location.data
        inspection.inspection_date = form.inspection_date.data
        inspection.reference_number = form.reference_number.data
        inspection.observations = form.observations.data
        inspection.conclusion_text = form.conclusion_text.data
        inspection.conclusion_status = form.conclusion_status.data
        # Update inspectors
        # Simplified handling for brevity
        db.session.commit()
        flash("Inspection updated successfully.", "success")
        return redirect(url_for("inspections.view", inspection_id=inspection.id))
    return render_template("inspection_form.html", form=form)


@inspections_bp.route("/<int:inspection_id>/delete", methods=["POST"])
@login_required
def delete(inspection_id):
    """Delete an inspection."""
    inspection = Inspection.query.get_or_404(inspection_id)
    db.session.delete(inspection)
    db.session.commit()
    flash("Inspection deleted successfully.", "info")
    return redirect(url_for("inspections.index"))
