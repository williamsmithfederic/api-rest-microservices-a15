import sqlite3
from modele.absence import Absence
from flask import Flask, jsonify, request

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
# SELECT ABSENCES
# =========================
@app.route("/v1/dao/absences", methods=["GET"])
def selectionner_absences():
    conn, curseur = get_connection()
    curseur.execute("""
        SELECT id, nom, prenom, type_absence,
               date_debut, date_fin, description, date_declaration
        FROM absences
        ORDER BY date_declaration DESC
    """)

    registre = []
    for rec in curseur.fetchall():
        absence = Absence(
            rec["id"],
            rec["nom"],
            rec["prenom"],
            rec["type_absence"],
            rec["date_debut"],
            rec["date_fin"],
            rec["description"],
            rec["date_declaration"]
        )
        registre.append(absence.to_dict())

    fermer_connection(conn)
    return jsonify({"data": registre})


# =========================
# INSERT ABSENCE
# =========================
@app.route("/v1/dao/absences", methods=["POST"])
def inserer_absence():
    data = request.get_json()

    conn, curseur = get_connection()
    curseur.execute("""
        INSERT INTO absences
        (nom, prenom, type_absence, date_debut, date_fin, description)
         VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["nom"],
        data["prenom"],
        data["type_absence"],
        data["date_debut"],
        data["date_fin"],
        data.get("description", "")
    ))
    conn.commit()
    fermer_connection(conn)

    return jsonify({"message": "absence insérée"}), 201

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    cde_ddl = """
    CREATE TABLE IF NOT EXISTS absences(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        type_absence TEXT NOT NULL,
        date_debut DATE NOT NULL,
        date_fin DATE NOT NULL,
        description TEXT,
        date_declaration DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    creer_bd(cde_ddl)
    app.run(port=5601, debug=True)
