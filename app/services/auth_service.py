from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request,
    get_jwt,
)
from app.models.user import User
from functools import wraps


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
            user = User.query.filter_by(email=user_data).first() if user_data else None
        else:
            user = (
                User.query.filter_by(username=user_data).first() if user_data else None
            )
    else:
        user = None

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        return None


def requires_roles(*roles):
    """
    Decorator function that verifies that the user making the request has the required roles.

    Args:
        *roles (list): A list of required roles.

    Returns:
        function: A decorator that can be applied to a view function. The decorated function will only be accessible to users with the required roles.
    """

    def wrapper(fn):
        """
        The wrapper function that wraps the original function.

        Args:
            fn (function): The original function to be decorated.

        Returns:
            function: The decorated function.
        """

        @wraps(fn)
        def decorator(*args, **kwargs):
            """
            The decorator function that wraps the original function and performs the role verification.

            Returns:
                object: The return value of the original function or a JSON response indicating that the user does not have the required roles.
            """
            verify_jwt_in_request()
            claims = get_jwt()
            if not set(roles).intersection(set(claims["roles"])):
                return jsonify(msg="Missing Authorization roles"), 403
            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper
