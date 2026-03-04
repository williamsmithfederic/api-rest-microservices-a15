from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

#============================================

# Pour autoriser le port :8000
CORS(app, resources={
    r"/stats/*": {
        "origins": "http://127.0.0.1:8000"
    }
})

#============================================

DAO_ABSENCE_URL = "http://127.0.0.1:5601/v1/dao/absences"
SRV_ABSENCE_URL = "http://127.0.0.1:5100/absences"
DAO_URL = "http://127.0.0.1:5600/v1/dao/incidents"
SRV_SERVICE_FAIT_URL = "http://127.0.0.1:5300/servicefait"



# ==========================
# STATS INCIDENTS (BI)
# ==========================
@app.route("/stats/incidents/by-type", methods=["GET"])
def stats_incidents_by_type():
    r = requests.get(DAO_URL)
    incidents = r.json()["data"]

    # Types métier autorisés
    TYPES_VALIDES = {
        "chute": "Chute",
        "panne": "Panne",
        "blessure": "Blessure",
        "incendie": "Incendie",
        "logistic": "Logistic",
        "autre": "Autre"
    }

    stats = {v: 0 for v in TYPES_VALIDES.values()}

    for i in incidents:
        raw = i.get("type_incident", "").strip().lower()

        if raw in TYPES_VALIDES:
            stats[TYPES_VALIDES[raw]] += 1

    # supprimer les catégories à 0
    labels = []
    values = []

    for k, v in stats.items():
        if v > 0:
            labels.append(k)
            values.append(v)

    return jsonify({
        "labels": labels,
        "values": values
    })
#============================
# STATS incident (BI) total
#============================

@app.route("/stats/incidents/total", methods=["GET"])
def stats_incidents_total():
    r = requests.get(DAO_URL)
    incidents = r.json().get("data", [])
    return jsonify({"total": len(incidents)})

# ==========================
# STATS ABSENCE (BI)
# ==========================


@app.route("/stats/absences/by-type", methods=["GET"])
def stats_absences_by_type():
    r = requests.get(DAO_ABSENCE_URL)
    absences = r.json()["data"]

    TYPES_VALIDES = {
        "maladie": "Maladie",
        "congé payé": "Congé payé",
        "congé sans solde": "Congé sans solde",
        "rendez-vous médical": "Rendez-vous médical",
        "autre": "Autre"
    }

    stats = {v: 0 for v in TYPES_VALIDES.values()}

    for row in absences:
        raw = row.get("type_absence", "").strip().lower()
        if raw in TYPES_VALIDES:
            stats[TYPES_VALIDES[raw]] += 1   # "total"

    # supprimer les catégories à 0
    labels = []
    values = []

    for k, v in stats.items():
        if v > 0:
            labels.append(k)
            values.append(v)

    return jsonify({
        "labels": labels,
        "values": values
    })

# ===========================
# STATS absence (BI) total

#============================

@app.route("/stats/absences/total", methods=["GET"])
def stats_absences_total():
    r = requests.get(DAO_ABSENCE_URL)
    absences = r.json().get("data", [])
    return jsonify({"total": len(absences)})

# ===========================
# STATS service FAIT (BI) total

#============================

@app.route("/stats/servicefait")
def stats_service_fait():

    try:
        response = requests.get(SRV_SERVICE_FAIT_URL)

        if response.status_code != 200:
            return jsonify({"error": "Service mobile indisponible"}), 500

        data = response.json()

        total_interventions = len(data)
        total_revenue = sum(float(s.get("total", 0)) for s in data)

        interventions_by_date = {}

        for s in data:

            date_value = s.get("date")

            if date_value:  #  évite None
                date = date_value.split(" ")[0]
                interventions_by_date[date] = interventions_by_date.get(date, 0) + 1

        return jsonify({
            "total_interventions": total_interventions,
            "total_revenue": total_revenue,
            "interventions_by_date": interventions_by_date
        })

    except Exception as e:
        print("BI ERROR:", e)
        return jsonify({"error": "Erreur serveur BI"}), 500


# ==========================
if __name__ == "__main__":
    app.run(debug=True, port=5200)
