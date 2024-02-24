from flask import request, Blueprint, jsonify
from app import db
from app.models.test_user import Test_User
from app.api import API_VERSION

auth_bp = Blueprint("auth", __name__, url_prefix=API_VERSION + "/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = Test_User.query.filter_by(username=data["username"]).first()
    if user:
        return jsonify({"message": "User already exists."}), 409

    new_user = Test_User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201
