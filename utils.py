import os
import logging
import jwt
from datetime import datetime, timedelta
from sendmail import SendMail

logger = logging.Logger(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
send = SendMail()

reset_token_collection = os.getenv('RESET_TOKEN_COLLECTION')


def password_reset(customer, domain):
    try:
        token = generate_token(customer['email'])
        reset_link = f"{domain}/api/v1/reset-password?token={token}"

        body = f"reset your password here: {reset_link}"
        subject = "Password Reset"
        send.send_email(receiver_email=customer['email'], subject=subject, body=body)
        return True
    except Exception as e:
        logger.exception("Server error: " + str(e))
        return False


def generate_token(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=20)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def validate_token(token):
    # Check if token is valid and not expired
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        expiration_time = payload['exp']
        email = payload['email']
        if datetime.utcnow() < datetime.utcfromtimestamp(expiration_time):
            return {'status': True, 'email': email}
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
