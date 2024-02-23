from flask import request, Blueprint, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        return jsonify({"message": "User already exists."}), 409

    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201
