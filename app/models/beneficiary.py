from app.models import db
from association import User_Beneficiary


class Beneficiary(db.Model):
    __tablename__ = "beneficiaries"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    account_number = db.Column(db.String)
    nickname = db.Column(db.String, nullable=True)
    bank_name = db.Column(db.String)
    is_verified = db.Column(db.Boolean)
    # Relation de retour vers User
    users = db.relationship(
        "User", secondary=User_Beneficiary, back_populates="beneficiaries"
    )
