"""PDF generation utilities using WeasyPrint."""
import os
from flask import current_app
from weasyprint import HTML
from jinja2 import Template

def generate_pdf(inspection):
    """
    Generate a PDF report for the given inspection.
    Returns the PDF bytes.
    """
    # Load HTML template
    template_dir = os.path.join(current_app.root_path, 'templates')
    html_template = os.path.join(template_dir, 'inspection_report.html')
    
    # Simple HTML content
    html_content = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 1cm; }}
            body {{ font-family: sans-serif; }}
            .header {{ text-align: center; margin-bottom: 1em; }}
            .section {{ margin-bottom: 1.5em; }}
            .photos {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1em; }}
            .photo {{ border: 1px solid #ccc; padding: 5px; }}
        </style>
    </head>
    <body>
        <div class="header"><h1>Inspection Report</h1></div>
        <div class="section"><strong>Reference:</strong> {{ reference_number }}</div>
        <div class="section"><strong>Version:</strong> {{ version }}</div>
        <div class="section"><strong>Installation:</strong> {{ installation_name }}</div>
        <div class="section"><strong>Location:</strong> {{ location }}</div>
        <div class="section"><strong>Date:</strong> {{ inspection_date.strftime('%Y-%m-%d') }}</div>
        <div class="section"><strong>Conclusion:</strong> {{ conclusion_text }}</div>
        <div class="section"><strong>Status:</strong> {{ conclusion_status }}</div>
        <div class="section"><strong>Observations:</strong> {{ observations }}</div>
        <div class="section"><strong>Inspectors:</strong>
            {% for inspector in inspectors %}
                {{ inspector.full_name or inspector.free_text_name }}, 
            {% endfor %}
        </div>
        <div class="section photos">
            {% for photo in photos %}
                <div class="photo"><img src="{{ filename }}" width="200"/>{{ caption }}</div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    
    # Generate PDF
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf()
    return pdf_bytes