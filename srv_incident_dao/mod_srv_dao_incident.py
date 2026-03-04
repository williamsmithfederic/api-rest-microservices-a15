import sqlite3
from flask import Flask, jsonify, request

from modele.mod_classes import Incident

app = Flask(__name__)

DB_PATH = "incidents.db"

# =========================
# UTILS BD
# =========================
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def fermer_connection(conn):
    conn.close()

def creer_bd(cde_ddl):
    conn, curseur = get_connection()
    curseur.execute(cde_ddl)
    conn.commit()
    fermer_connection(conn)

# =========================
# SELECT INCIDENTS
# =========================
@app.route("/v1/dao/incidents", methods=["GET"])
def selectionner_incidents():
    conn, curseur = get_connection()
    curseur.execute("""
        SELECT id, nom, prenom, type_incident, priorite, statut, description, date_incident, date_cloture, description_admin
        FROM incidents
        ORDER BY id DESC
    """)
    registre = []
    for rec in curseur.fetchall():
        registre.append(
            Incident(
                rec["id"],
                rec["nom"],
                rec["prenom"],
                rec["type_incident"],
                rec["priorite"],
                rec["statut"],
                rec["description"],
                rec["date_incident"],
                rec["date_cloture"],
                rec["description_admin"]
        ).__dict__
        )
    fermer_connection(conn)
    return jsonify({"data": registre})

# =========================
# INSERT INCIDENT
# =========================
@app.route("/v1/dao/incidents", methods=["POST"])
def inserer_incident():
    data = request.get_json()

    conn, curseur = get_connection()
    curseur.execute("""
        INSERT INTO incidents(
        nom, 
        prenom, 
        type_incident, 
        priorite, 
        statut, 
        description, 
        date_incident
        )
        VALUES (?, ?, ?, ?, 'Ouvert', ?, datetime('now'))
    """, (
        data["nom"],
        data["prenom"],
        data["type_incident"],
        data["priorite"],
        data["description"]

    ))
    conn.commit()
    fermer_connection(conn)
    return jsonify({"message": "incident inséré avec statut Ouvert"}), 201


#========================================
#  Update Status
#========================================

@app.route("/v1/dao/incidents/<int:id>/statut", methods=["POST"])
def update_statut(id):
    data = request.get_json()
    statut = data["statut"]
    description_admin = data.get("description_admin", "")

    conn, curseur = get_connection()

    # Si statut = Clos, mettre à jour date_cloture automatiquement
    if statut == "Clos":
        curseur.execute("""
            UPDATE incidents
            SET statut = ?, date_cloture = datetime('now'), description_admin = ?
            WHERE id = ?
        """, (statut, description_admin, id))
    else:
        curseur.execute("""
            UPDATE incidents
            SET statut = ?, date_cloture = NULL, description_admin = ?
            WHERE id = ?
        """, (statut, description_admin, id))

    conn.commit()
    fermer_connection(conn)

    return jsonify({"message": "statut mis à jour"})

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    cde_ddl = """
    CREATE TABLE IF NOT EXISTS incidents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prenom TEXT,
        type_incident TEXT,
        priorite TEXT,
        statut TEXT,
        description TEXT,
        date_incident TEXT,
        date_cloture TEXT,
        description_admin TEXT
    )
    """
    creer_bd(cde_ddl)
    app.run(port=5600, debug=True)
