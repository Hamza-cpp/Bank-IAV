import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///bank.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("DB_TRACK_MODIFICATIONS", False)
    API_VERSION = os.getenv("API_VERSION", "/api/v1")
