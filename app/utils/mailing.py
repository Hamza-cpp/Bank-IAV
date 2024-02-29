from app import mail
from flask import render_template, url_for, current_app, jsonify
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer


def send_verification_email(user):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(
        user.email, salt=current_app.config["SECURITY_PASSWORD_SALT"]
    )

    confirm_url = url_for("auth.confirm_email", token=token, _external=True)

    # Email content
    msg = Message("Verify Your Email Address", recipients=[str(user.email)])
    msg.html = render_template(
        "verification_email.html", username=user.username, confirm_url=confirm_url
    )
    mail.send(msg)
    print("message: Verification email sent successfully!")
