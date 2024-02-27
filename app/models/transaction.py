from app.models import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    transaction_type = db.Column(db.String)  # DEPOSIT, TRANSFER, WITHDRAWAL
    related_transaction_id = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Numeric(10, 2))
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    initiated_by = db.Column(db.String, nullable=True)
    # Relation to Account
    account = db.relationship("Account", back_populates="transactions")