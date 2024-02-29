from flask_jwt_extended import jwt_required
from flask import jsonify, Blueprint
from app.models.role import Role, ADMIN_ROLE, CLIENT_ROLE
from app.models.account import ACTIVE_ACCOUNT, SUSPENDED_ACCOUNT, Account
from app.services.auth_service import requires_roles
from app import db
from app.api import API_VERSION
from app.utils.validators import (
    is_valid_email,
    is_valid_role,
    is_valid_account_status,
    is_valid_email,
)

admin_bp = Blueprint("admin", __name__, url_prefix=API_VERSION + "/admin")


@admin_bp.route(
    "/update_account_status/<integer:accountID>/<string:status>", methods=["PUT"]
)
@jwt_required()
@requires_roles(ADMIN_ROLE)
def update_account_status(accountID, status):
    """
    Update the account status of a user.

    Args:
        accountID (int): The ID of the user's account to update.
        status (str): The new status of the user's account. Must be either 'active' or 'suspended'.

    Returns:
        JSON: A JSON response indicating whether the account was updated successfully.
            If the account status is successfully updated, a success message is returned.
            If the provided status is invalid, an error message is returned.
            If the account with the provided ID is not found, a '404 Not Found' error message is returned.

    Raises:
        None
    """
    if not is_valid_account_status(status):
        return (
            jsonify(
                {
                    "error": f"Invalid status. Use '{ACTIVE_ACCOUNT}' or '{SUSPENDED_ACCOUNT}'."
                }
            ),
            422,
        )

    account_to_update = Account.query.get(accountID).first()
    if not account_to_update:
        return jsonify({"message": "Account not found"}), 404

    account_to_update.status = status
    db.session.commit()

    action = "activated" if status == ACTIVE_ACCOUNT else "deactivated"
    return (
        jsonify(
            {
                "message": f"Account ID {account_to_update.account_id} has been successfully {action}."
            }
        ),
        200,
    )


@admin_bp.route(
    "/users/<string:email>/assign-role/<string:role_name>", methods=["POST"]
)
@jwt_required()
@requires_roles(ADMIN_ROLE)
def assign_role(email, role_name):
    """
    This function assigns a role to a user.

    :param email: The email of the user to update.
    :param role_name: The name of the role to assign. Must be either 'admin' or 'client'.
    :return: A message indicating whether the role was assigned successfully.
    """
    if not is_valid_email(email=email):
        return (
            jsonify({"message": "Invalid email formate."}),
            400,
        )
    if not is_valid_role(role_name):
        return (
            jsonify(
                {
                    "message": f"Invalid role name. Use '{ADMIN_ROLE}' or '{CLIENT_ROLE}'."
                }
            ),
            400,
        )
    user_obj = User.query.filter_by(email=email).first()
    if not user_obj:
        return jsonify({"message": "User not found"}), 404
    role_obj = Role.query.filter_by(name=role_name).first()
    if not role_obj:
        role_obj = Role(name=role_name)
        db.session.add(role_obj)

    user_obj.roles.append(role_obj)
    db.session.commit()

    return jsonify({"message": f"{role_name} assigned successfully."}), 200
