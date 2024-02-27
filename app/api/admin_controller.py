from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import jsonify, Blueprint
from app.models.user import User
from app.services.auth_service import requires_roles
from app import db

bp = Blueprint('user_blueprint', __name__)

@bp.route('/update_account_status/<string:username>/<string:status>', methods=['PUT'])
@jwt_required()
# @requires_roles("admin")
def update_account_status(username, status):
    current_user_id = get_jwt_identity()
    admin_user = User.query.get(current_user_id)

    if status not in ['activate', 'deactivate']:
        return jsonify({"message": "Invalid status. Use 'activate' or 'deactivate'."}), 400

    user_to_update = User.query.filter_by(username=username).first()
    if not user_to_update:
        return jsonify({"message": "User not found"}), 404

    user_to_update.is_active = (status == 'activate')
    db.session.commit()

    action = "activated" if status == 'activate' else "deactivated"
    return jsonify({"message": f"User {user_to_update.username} has been successfully {action}."}), 200