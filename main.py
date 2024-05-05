from flask import Flask, request, jsonify
from auth import auth_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"health": "OK"}), 200


if __name__ == "__main__":
    app.run(debug=True)