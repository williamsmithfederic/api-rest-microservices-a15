from flask import Flask, request, jsonify
import requests
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "secret_key"
DAO_AUTH_URL = "http://127.0.0.1:5603"


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"success": False}), 400

    response = requests.post(
        f"{DAO_AUTH_URL}/login",
        json=data
    )

    if response.status_code != 200:
        return jsonify({"success": False}), 401

    dao_data = response.json()

    # Génération token JWT
    token = jwt.encode({
        "employe_id": dao_data["employe_id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "success": True,
        "token": token
    }), 200


if __name__ == "__main__":
    app.run(port=5400, debug=True)