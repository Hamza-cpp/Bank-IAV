from app.models import db
from datetime import datetime
from app.models.association import User_Role, User_Beneficiary
from app.models.beneficiary import Beneficiary
from app.models.role import Role
from app.models.user_profile import UserProfile
from app.models.account import Account
from app.models.loan_application import LoanApplication
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column("username", db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    # Relations
    profile = db.relationship("UserProfile", back_populates="user", uselist=False)
    accounts = db.relationship("Account", back_populates="user")
    loan_applications = db.relationship("LoanApplication", back_populates="user")
    beneficiaries = db.relationship(
        "Beneficiary",
        secondary=User_Beneficiary,
        back_populates="users",
    )
    roles = db.relationship("Role", secondary=User_Role, back_populates="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
