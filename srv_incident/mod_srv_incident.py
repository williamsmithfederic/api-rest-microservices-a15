from flask import Flask, request, jsonify
from flasgger import Swagger
import requests

app = Flask(__name__)

# 🔹 Configuration Swagger
swagger = Swagger(app)

DAO_URL = "http://127.0.0.1:5600/v1/dao/incidents"


# ==========================
# TEST
# ==========================
@app.route("/")
def test():
    """
    Test Service
    ---
    responses:
      200:
        description: Service Incident is running
    """
    return "SRV INCIDENT OK"


# ==========================
# INSERT INCIDENT
# ==========================
@app.route("/incidents", methods=["POST"])
def creer_incident():
    """
    Create Incident
    ---
    tags:
      - Incidents
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nom:
              type: string
            prenom:
              type: string
            type_incident:
              type: string
            priorite:
              type: string
    responses:
      201:
        description: Incident created
    """
    data = request.get_json()
    r = requests.post(DAO_URL, json=data)

    return jsonify({"message": "Incident créé"}), 201


# ==========================
# LIST INCIDENTS
# ==========================
@app.route("/incidents", methods=["GET"])
def lister_incidents():
    """
    Get All Incidents
    ---
    tags:
      - Incidents
    responses:
      200:
        description: List of incidents
    """
    r = requests.get(DAO_URL)
    return jsonify(r.json())


# ==========================
# UPDATE STATUT
# ==========================
@app.route("/incidents/<int:id>/statut", methods=["POST"])
def update_statut_incident(id):
    """
    Update Incident Status
    ---
    tags:
      - Incidents
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            statut:
              type: string
            description_admin:
              type: string
    responses:
      200:
        description: Status updated
    """
    data = request.get_json()
    r = requests.post(f"{DAO_URL}/{id}/statut", json=data)

    if r.status_code == 200:
        return jsonify({"message": "Statut mis à jour"}), 200
    else:
        return jsonify({"error": "Erreur"}), 500


# ==========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)