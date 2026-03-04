from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ==========================================

DAO_ABSENCE_URL = "http://127.0.0.1:5601/v1/dao/absences"
SRV_ABSENCE_URL = "http://127.0.0.1:5100/absences"


# ==========================
# INSERT (client_absence
# ==========================


@app.route("/absences", methods=["POST"])
def creer_absence():
    data = request.get_json()

    # forward vers DAO
    r = requests.post(DAO_ABSENCE_URL, json=data)

    return jsonify({"message": "Absence créé"}), 201

# ==========================
# SELECT (client_admin)
# =========================

@app.route("/absences", methods=["GET"])
def lister_absences():
    r = requests.get(DAO_ABSENCE_URL)
    return jsonify(r.json())


#===========================
if __name__ == "__main__":
    app.run(port=5100, debug=True)
