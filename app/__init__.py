from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
from app.models import db
from app.models.user import User

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)
    jwt = JWTManager(app)
    mail.init_app(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        """
        This function is used to retrieve the user from the database and add their roles as claims to the access token.

        :param identity: The identity of the user
        :type identity: int
        :return: A dictionary containing the roles of the user, or None
        """
        user = User.query.get(identity)
        if not user:
            return None
        return {"roles": [role.name for role in user.roles]}

    from app.api.auth import auth_bp
    from app.api.user_controller import user_bp
    from app.api.admin_controller import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    # app.register_blueprint(user.bp)
    # app.register_blueprint(account.bp)

    return app
