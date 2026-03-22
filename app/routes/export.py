"""Export blueprint for PDF generation."""

from flask import Blueprint, render_template_string, send_file, current_app
from flask_login import login_required, current_user
from app.models import Inspection
from app.utils.pdf_generator import generate_pdf

export_bp = Blueprint("export", __name__)


@export_bp.route("/inspection/<int:inspection_id>/pdf")
@login_required
def inspection_pdf(inspection_id):
    """Generate and download PDF for an inspection."""
    # Ensure the user has access to the inspection
    inspection = Inspection.query.get_or_404(inspection_id)
    # Check that current user is inspector or admin
    allowed = current_user.id == inspection.created_by or current_user.is_admin
    if not allowed:
        from flask import abort

        abort(403)

    pdf_bytes = generate_pdf(inspection_id)
    # Create a temporary file to serve
    from pathlib import Path
    import tempfile
    import os

    # Use a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        return send_file(
            tmp_path,
            as_attachment=True,
            download_name=f"inspection_report_{inspection.reference_number}_v{inspection.version}.pdf",
            mimetype="application/pdf",
        )
    finally:
        # Clean up the temporary file
        os.unlink(tmp_path)
