from app.models import db

User_Role = db.Table(
    "users_roles",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    ),
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id"),
        primary_key=True,
        nullable=False,
    ),
)

User_Beneficiary = db.Table(
    "users_beneficiaries",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    ),
    db.Column(
        "beneficiary_id",
        db.Integer,
        db.ForeignKey("beneficiaries.id"),
        primary_key=True,
        nullable=False,
    ),
)
