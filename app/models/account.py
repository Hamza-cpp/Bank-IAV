from app.models import db
import datetime

class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    account_number = db.Column(db.String)
    account_type = db.Column(db.String)
    balance = db.Column(db.Numeric(10, 2))
    opened_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String, default="ACTIVE")  # eg. ACTIVE, SUSPENDED
    # Relations
    user = db.relationship("User", back_populates="accounts")
    transactions = db.relationship("Transaction", back_populates="accounts")