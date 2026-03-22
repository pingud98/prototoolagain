# Inspection Reporting and Management App

## Project Overview
This is a production-ready Inspection Reporting and Management web application built with Python 3.11+, Flask, SQLite, and WeasyPrint for PDF generation.

## Requirements
- Python 3.11 or higher
- pip
- System dependencies for WeasyPrint (e.g., libpango, libharfbuzz, etc.)

## Setup
1. Install Python dependencies: `pip install -r requirements.txt`
2. Run the setup script: `python setup.py`
   - This installs dependencies, generates a self-signed TLS certificate, creates the SQLite database, and prompts for admin account details.
3. Ensure system-level WeasyPrint dependencies are installed:
   - Debian/Ubuntu: `sudo apt install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`
   - macOS: `brew install pango`
   - Windows: Follow instructions at https://doc.courtbouillon.org/weasyprint/stable/first_steps.html

## Running the Application
1. Start the server: `python run.py`
2. Access the application at `https://localhost:5000`
   - Due to the self-signed certificate, your browser will show a warning. You can proceed by adding an exception or using `--no-check-certificates` if supported.

## Authentication
- Login with the admin account created during setup.
- All routes are protected; unauthenticated access redirects to the login page.
- Logout is available via the `/logout` route.

## Admin Panel
- Accessible at `/admin`.
- Admins can manage users, view inspections, and perform administrative tasks.
- Only users with `is_admin=True` can access the admin panel.

## PDF Export
- Inspection reports can be exported as PDFs via the `/inspection/<id>/pdf` endpoint.
- PDFs are generated using WeasyPrint and formatted for A4 pages.

## Security
- Passwords are hashed with bcrypt (cost factor 12).
- CSRF protection is enabled on all forms.
- File uploads are validated for allowed types and size limits.
- Input is escaped in templates.

## Notes
- The self-signed certificate may cause browser warnings. For production, consider using a trusted certificate or `mkcert` for local development.
- All database files, environment variables, and certificates are listed in `.gitignore`.