"""PDF generation utility."""

from flask import current_app
from weasyprint import HTML
from pathlib import Path
from flask import render_template, url_for
from app.models import Inspection


def generate_pdf(inspection_id):
    """Render inspection view template and convert to PDF."""
    inspection = Inspection.query.get_or_404(inspection_id)
    inspectors = inspection.inspectors
    photos = inspection.photos
    # Render the inspection view template
    html = render_template(
        "inspection_view.html",
        inspection=inspection,
        inspectors=inspectors,
        photos=photos,
    )
    # Generate PDF
    pdf_bytes = HTML(string=html, base_url=current_app.root_path).write_pdf()
    return pdf_bytes
