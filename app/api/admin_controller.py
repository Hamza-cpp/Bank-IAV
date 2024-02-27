from flask_jwt_extended import jwt_required
from flask import jsonify, Blueprint
from app.models.user import User
from app.models.role import Role, ADMIN_ROLE, CLIENT_ROLE
from app.models.account import ACTIVE_ACCOUNT, SUSPENDED_ACCOUNT
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
    "/update_account_status/<string:email>/<string:status>", methods=["PUT"]
)
@jwt_required()
@requires_roles(ADMIN_ROLE)
def update_account_status(email, status):
    """
    This function updates the account status of a user.

    :param email: The email of the user to update.
    :param status: The new status of the user's account. Must be either 'active' or 'suspended'.
    :return: A message indicating whether the user was updated successfully.
    """
    if not is_valid_account_status(status):
        return (
            jsonify(
                {
                    "message": f"Invalid status. Use '{ACTIVE_ACCOUNT}' or '{SUSPENDED_ACCOUNT}'."
                }
            ),
            400,
        )
    if not is_valid_email(email=email):
        return (
            jsonify({"message": "Invalid email formate."}),
            400,
        )

    user_to_update = User.query.filter_by(email=email).first()
    if not user_to_update:
        return jsonify({"message": "User not found"}), 404

    user_to_update.is_active = status == ACTIVE_ACCOUNT
    db.session.commit()

    action = "activated" if status == ACTIVE_ACCOUNT else "deactivated"
    return (
        jsonify(
            {"message": f"User {user_to_update.email} has been successfully {action}."}
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
