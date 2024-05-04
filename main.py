from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"health": "OK"}), 200


if __name__ == "__main__":
    app.run(debug=True)