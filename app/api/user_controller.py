from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account import Account
from app.models.user import User
from app.api import API_VERSION


accounts_bp = Blueprint("accounts", __name__, url_prefix=API_VERSION + "/accounts")


@accounts_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard_summary():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user:
        return jsonify({"error": "User not found or not active."}), 403

    accounts = Account.query.filter_by(user_id=current_user_id).all()
    if not accounts:
        return jsonify({"message": "No accounts found for this user."}), 200

    accounts_summary = [acc.serialize() for acc in accounts]

    return jsonify({"accounts": accounts_summary}), 200


def serialize(self):
    """
    Returns a dictionary containing the account's information.

    Parameters:
        self (Account): The instance of the Account class to be serialized.

    Returns:
        dict: A dictionary containing the account's information.
    """
    return {
        "account_number": self.account_number,
        "account_type": self.account_type,
        "balance": str(self.balance),
        "status": self.status,
        "open_at": str(self.open_at),
        "close_at": str(self.close_at),
    }
