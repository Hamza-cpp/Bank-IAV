import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("DB_TRACK_MODIFICATIONS")
    API_VERSION = os.getenv("API_VERSION")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    TEMPLATES_AUTO_RELOAD = os.getenv("TEMPLATES_AUTO_RELOAD")
