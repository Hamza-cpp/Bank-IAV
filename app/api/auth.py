from flask import request, Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app import db
from app.api import API_VERSION
from app.models.user import User
from app.services.auth_service import authenticate_user, requires_roles
from app.utils.validators import is_valid_email
from app.utils.mailing import send_verification_email

auth_bp = Blueprint("auth", __name__, url_prefix=API_VERSION + "/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    Returns:
        JSON: A JSON response containing a success message if the user is successfully registered,
        or an error message if registration fails.
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "Username, email, and password are required"}), 422
    if not is_valid_email(email=email):
        return jsonify({"msg": "Email is invalide"}), 422

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
        db.session.rollback()
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500
    try:
        send_verification_email(new_user)

    except Exception as e:
        print("An error occurred while sending the email", str({e}))
        db.session.rollback()
        return (
            jsonify(
                {"msg": "An error occurred while sending the email.", "error": str(e)}
            ),
            500,
        )

    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in a user.

    Returns:
        JSON: A JSON response containing an authentication token if the login is successful,
        or an error message if authentication fails.
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not (username or email):
        return jsonify({"msg": "Missing username or email"}), 422
    if not password:
        return jsonify({"msg": "Missing password"}), 422

    if username and email:
        return jsonify({"msg": "Provide either username or email, not both"}), 422

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


@auth_bp.route("/transfer", methods=["POST"])
@jwt_required()
@requires_roles("client", "admin")
def transfer_money():
    # Your money transfer logic here
    return jsonify({"msg": "Money transferred successfully"})


@auth_bp.route("/confirm_email/<token>", methods=["GET"])
def confirm_email(token):
    """
    Confirm the email address associated with the provided verification token.

    Args:
        token (str): The verification token sent to the user's email address.

    Returns:
        JSON: A JSON response indicating the result of the email verification process.
            If the email is successfully verified, a success message is returned.
            If the token is expired or invalid, an appropriate error message is returned.
            If an unexpected error occurs during verification, a generic error message is returned.

    Raises:
        None
    """
    duration = 3600  # Token expires after 1 hour
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=duration
        )
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_active = True
            db.session.commit()
            return jsonify({"msg": "Email successfully verified!"})
        else:
            return (
                jsonify(
                    {
                        "error": "The email address associated with this token does not exist in our system."
                    }
                ),
                400,
            )
    except SignatureExpired:
        return (
            jsonify(
                {
                    "error": "The verification token has expired. Please request a new verification email."
                }
            ),
            400,
        )
    except BadSignature:
        return jsonify({"error": "The verification token is invalid."}}), 400
    except Exception as e:
        print(f"An error occurred during email verification: {str(e)}")
        return jsonify({"error": "An error occurred during verification."}), 500
