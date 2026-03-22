from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CsrfProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

csrf = CsrfProtect()
csrf.init_app(app)
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    limiter = Limiter(key_func=get_remote_address)
    limiter.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.inspections import inspections_bp
    from app.routes.admin import admin_bp
    from app.routes.export import export_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inspections_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(export_bp)

    # Create database tables if they don't exist
    @app.before_first_request
    def create_tables():
        db.create_all()

    # Configure audit logging
    import logging
    from logging.handlers import RotatingFileHandler
    import os

    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("audit")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        "logs/audit.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    formatter = logging.Formatter("SECURITY AUDIT: %(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return app
