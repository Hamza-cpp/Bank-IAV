from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.test_user import Test_User


def authenticate_user(user_data, password):
    """
    Authenticates a user based on provided data and password.

    Args:
        user_data (str): The user's username or email.
        password (str): The user's password.

    Returns:
        dict: A dictionary containing access and refresh tokens if successful, None otherwise.
    """
    if isinstance(user_data, str):
        if "@" in user_data:  # Explicitly check for "@" symbol
            user = (
                Test_User.query.filter_by(email=user_data).first()
                if user_data
                else None
            )
        else:
            user = (
                Test_User.query.filter_by(username=user_data).first()
                if user_data
                else None
            )
    else:
        user = None

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        return None
