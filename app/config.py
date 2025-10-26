import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY missing")
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
