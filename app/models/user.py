from models import db
import datetime
from association import User_Role, User_Beneficiary


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column("username", db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean)
    # Relations
    profiles = db.relationship("UserProfile", back_populates="users", uselist=False)
    accounts = db.relationship("Account", back_populates="users")
    loan_applications = db.relationship("LoanApplication", back_populates="users")
    beneficiaries = db.relationship(
        "Beneficiary",
        secondary=User_Beneficiary,
        back_populates="users",
    )
    roles = db.relationship("Role", secondary=User_Role, back_populates="users")
