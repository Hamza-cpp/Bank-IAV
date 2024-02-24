from app.models import db
from association import User_Role


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    # Relation many to many Role <--> User
    users = db.relationship("User", secondary=User_Role, back_populates="roles")
