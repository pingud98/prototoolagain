"""Entry point for running the Flask application."""

import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Use TLS context for HTTPS
    app.run(host="0.0.0.0", port=5000, ssl_context="adhoc")
