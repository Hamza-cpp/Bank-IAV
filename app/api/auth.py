from flask import request, Blueprint, jsonify
from app.services.auth_service import authenticate_user, requires_roles
from app import db
from app.models.user import User
from app.api import API_VERSION
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix=API_VERSION + "/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "Username, email, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User with given email already exists"}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User with given username already exists"}), 409

    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(f"An error occurred during user registration: {e}")
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500

    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not (username or email):
        return jsonify({"msg": "Missing username or email"}), 400
    if not password:
        return jsonify({"msg": "Missing password"}), 400

    if username and email:
        return jsonify({"msg": "Provide either username or email, not both"}), 400

    if email:
        user_data = email
        login_method = "email"
    else:
        user_data = username
        login_method = "username"

    authentication = authenticate_user(user_data, password)

    if authentication:
        return jsonify(authentication), 200
    else:
        return jsonify({"msg": f"Invalid {login_method} or password"}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    Endpoint to refresh an access token using a refresh token.

    Returns:
        JSON: A dictionary containing a new access token if successful, error message otherwise.
    """
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return jsonify({"access_token": new_access_token}), 200
    except Exception as e:
        return jsonify({"message": "Token refresh failed", "error": str(e)}), 500


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Endpoint to refresh an access token using a refresh token.

    Returns:
        JSON: A dictionary containing a new access token if successful, error message otherwise.
    """
    return jsonify({"msg": "welcome"})


@auth_bp.route("/transfer", methods=["POST"])
@jwt_required()
@requires_roles("client","admin")
def transfer_money():
    # Your money transfer logic here
    return jsonify({"msg": "Money transferred successfully"})
