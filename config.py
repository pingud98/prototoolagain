class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/inspection.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
    REMEMBER_COOKIE_DURATION = 86400
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
