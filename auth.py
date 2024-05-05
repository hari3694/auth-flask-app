import os
import logging
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from mongo_manager import MongoManager
from utils import password_reset, validate_token
from dotenv import load_dotenv
from decorators import login_required

load_dotenv()
logger = logging.Logger(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__)
AUTH_DB = os.getenv('AUTH_DB')
SECRET_KEY = os.getenv('SECRET_KEY')


mongo = MongoManager(AUTH_DB)
customer_collection = os.getenv('AUTH_COLLECTION')


@auth_blueprint.route("/api/v1/login", methods=['POST'])
def login():
    try:
        body = request.json
        domain = request.host_url
        if 'email' in body:
            email = body['email']
            customer = mongo.find_one(customer_collection, {'email': email})
            if customer:
                if 'password' in customer:
                    if 'password' not in body:
                        return jsonify({'message': 'Missing email or password'}), 400
                    else:
                        if customer['password'] == body['password']:
                            token = jwt.encode({'customer_id': customer['customer_id'], 'customer_email': customer['email'],
                                                'exp': datetime.utcnow() + timedelta(days=30)},
                                               key=SECRET_KEY, algorithm="HS256")
                            return jsonify({'token': token}), 200
                else:
                    password_reset(customer, domain)
                    return jsonify({'message': f'Link to reset the password have been sent to {email}'}), 400
            else:
                return jsonify({'message': 'User not found'}), 404
        else:
            return jsonify({'message': 'Missing email or password'}), 400
    except Exception as E:
        logger.exception(str(E))
        return 500


@auth_blueprint.route('/api/v1/forgot-password', methods=['POST'])
def forgot_password():
    try:
        domain = request.host_url
        body = request.json
        if 'email' in body:
            email = body['email']
            customer = mongo.find_one(customer_collection, {'email': email})
            if customer:
                reset = password_reset(customer, domain)
            return jsonify({'message': f'Link to reset the password have been sent to {email}'}), 400
        return jsonify({'message': 'Missing email'}), 400
    except Exception as E:
        logger.exception(str(E))
        return 500


@auth_blueprint.route('/api/v1/reset-password', methods=['POST'])
def reset_password():
    try:
        token = request.args.get('token')
        new_password = request.json.get('new_password')

        if token:
            validate = validate_token(token)
            if validate:
                email = validate['email']
                mongo.update_one(customer_collection, {'email': email}, {'password': new_password})
                return jsonify({'message': 'Password reset successful'})
            else:
                return jsonify({'error': 'Token has expired'}), 400
        else:
            return jsonify({'error': 'Invalid token'}), 400
    except Exception as E:
        logger.exception(str(E))
        return 500
