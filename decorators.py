from functools import wraps
from flask import request, jsonify
import jwt
import os
import  logging
import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.Logger(__name__)

AUTH_DB = os.getenv('AUTH_DB')
SECRET_KEY = os.getenv('SECRET_KEY')


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Check if Authorization header is present
            token = request.headers.get('Authorization')
            if not token:
                raise jwt.InvalidTokenError('Token is missing')

            # Check if token is valid
            payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=['HS256'])
            current_time = datetime.datetime.utcnow()
            expiration_time = datetime.datetime.utcfromtimestamp(payload['exp'])
            if current_time > expiration_time:
                raise jwt.ExpiredSignatureError('Token has expired')
            email = payload['customer_email']

            return func(email, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'message': str(e)}), 401
        except Exception as e:
            logger.exception(str(e))
            return jsonify({'message': 'An unexpected error occurred'}), 500

    return wrapper
