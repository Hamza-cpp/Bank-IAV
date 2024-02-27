from app.models import db
from datetime import datetime


class LoanApplication(db.Model):
    __tablename__ = "loan_applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    loan_type = db.Column(db.String)
    amount_requested = db.Column(db.Numeric(10, 2))
    duration = db.Column(db.Integer)
    interest_rate = db.Column(db.Numeric(5, 2))
    monthly_payment = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String, default="SUBMETED")  # SUBMETED, PENDING, APPROVED, REJECTED
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_by = db.Column(db.String, nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    # Relation to User
    user = db.relationship("User", back_populates="loan_applications")
