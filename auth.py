import os
import logging
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from mongo_manager import MongoManager
from utils import password_reset
from dotenv import load_dotenv

load_dotenv()
logger = logging.Logger(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__)
AUTH_DB = os.getenv('AUTH_DB')
SECRET_KEY = os.getenv('SECRET_KEY')


mongo = MongoManager(AUTH_DB)
collection = os.getenv('AUTH_COLLECTION')


@auth_blueprint.route("/api/v1/login", methods=['POST'])
def select_operation():
    body = request.json
    if 'email' in body:
        email = body['email']
        customer = mongo.find_one(collection, {'email': email})
        if customer:
            if 'password' in customer:
                if 'password' not in body:
                    return jsonify({'message': 'Missing email or password'}), 400
                else:
                    if customer['password'] == body['password']:
                        token = jwt.encode({'customer_id': customer['customer_id'],
                                            'exp': datetime.utcnow() + timedelta(days=30)},
                                           key=SECRET_KEY, algorithm="HS256")
                        return jsonify({'token': token}), 200
            else:
                password_reset(email)
                return jsonify({'message': f'Link to reset the password have been sent to {email}'}), 400
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Missing email or password'}), 400
