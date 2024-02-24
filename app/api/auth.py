from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token
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


@auth_bp.route("/registerjwt", methods=["POST"])
def registerJwt():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "Username, email, and password are required"}), 400

    if (
        Test_User.query.filter_by(username=username).first()
        or Test_User.query.filter_by(email=email).first()
    ):
        return jsonify({"msg": "User with given email/username already exists"}), 409

    new_user = Test_User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = Test_User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=[username,password])
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401
