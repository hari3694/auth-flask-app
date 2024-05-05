from flask import Flask, request, jsonify
from auth import auth_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Auth API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

AUTH_NOT_REQUIRED_ENDPOINTS = ['/api/v1/login', '/api/v1/forgot-password', '/api/v1/reset-password', '/healthcheck']
NON_MIN_VERSION_ENDPOINTS = ['/api/v1/reset-password', '/healthcheck']
MIN_VERSION = '2.1.0'

@app.before_request
def before_request():
    # Check if the endpoint requires authentication
    if 'swagger' not in request.path:
        if request.path not in AUTH_NOT_REQUIRED_ENDPOINTS:
            # Check if the token is present and valid
            token = request.headers.get('Authorization')
            if not token:

                return jsonify({'message': 'Token is missing'}), 401

        # Check if the endpoint requires minimum version
        if request.path not in NON_MIN_VERSION_ENDPOINTS:
            client_version = request.headers.get('Client-Version')
            if not client_version or client_version < MIN_VERSION:
                return jsonify({'message': 'Minimum version requirement not met'}), 403


app.register_blueprint(auth_blueprint)


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"health": "OK"}), 200


if __name__ == "__main__":
    app.run(debug=True)