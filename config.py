import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-' + str(os.getpid())
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "inspection.db"}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    # File upload config
    UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB per file
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}