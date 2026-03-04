from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DAO_URL = "http://127.0.0.1:5602"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    response = requests.post(f"{DAO_URL}/login", json=data)
    return jsonify(response.json()), response.status_code


@app.route("/servicefait", methods=["POST"])
def insert_intervention():
    data = request.json
    response = requests.post(f"{DAO_URL}/servicefait", json=data)
    return jsonify(response.json()), response.status_code


@app.route("/clients", methods=["GET"])
def get_clients():
    response = requests.get(f"{DAO_URL}/clients")
    return jsonify(response.json()), response.status_code

@app.route("/services", methods=["GET"])
def get_services():
    response = requests.get(f"{DAO_URL}/services")
    return jsonify(response.json()), response.status_code

@app.route("/servicefait", methods=["GET"])
def get_interventions():

    try:
        # 1 Appel du DAO (5602)
        response = requests.get(f"{DAO_URL}/servicefait")

        # 2️ Si le DAO répond correctement
        if response.status_code == 200:

            data = response.json()   # ← ici on récupère la liste
            return jsonify(data), 200

        # 3️ Si le DAO renvoie une erreur
        else:
            print("DAO ERROR STATUS:", response.status_code)
            print("DAO RESPONSE:", response.text)
            return jsonify([]), 200

    except Exception as e:
        print("ERROR CALLING DAO:", e)
        return jsonify([]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5300, debug=True)