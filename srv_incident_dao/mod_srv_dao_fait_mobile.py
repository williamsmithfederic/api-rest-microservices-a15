from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "incidents.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==============================
# 🔹 LISTER LES SERVICES
# ==============================
@app.route('/services', methods=['GET'])
def get_services():
    conn = get_connection()
    services = conn.execute("SELECT * FROM service").fetchall()
    conn.close()
    return jsonify([dict(row) for row in services])


# ==============================
# 🔹 CREER UNE INTERVENTION
# ==============================
@app.route('/servicefait', methods=['POST'])
def create_service_fait():

    data = request.json

    employe_id = data['employe_id']
    client_id = data['client_id']
    commentaire = data['commentaire']
    services = data['services']  # liste des IDs

    conn = get_connection()
    cursor = conn.cursor()

    # 1️⃣ Calcul total
    total = 0
    for service_id in services:
        row = cursor.execute(
            "SELECT prix FROM service WHERE id=?",
            (service_id,)
        ).fetchone()
        total += row["prix"]

    # 2️⃣ Insert intervention
    cursor.execute("""
        INSERT INTO service_fait (employe_id, client_id, commentaire, total, date)
        VALUES (?, ?, ?, ?, datetime('now'))
    """, (employe_id, client_id, commentaire, total))

    service_fait_id = cursor.lastrowid

    # 3️⃣ Insert détails
    for service_id in services:
        row = cursor.execute(
            "SELECT prix FROM service WHERE id=?",
            (service_id,)
        ).fetchone()

        cursor.execute("""
            INSERT INTO service_fait_detail
            (service_fait_id, service_id, prix)
            VALUES (?, ?, ?)
        """, (service_fait_id, service_id, row["prix"]))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Intervention enregistrée",
        "total": total
    }), 201

@app.route('/clients', methods=['GET'])
def get_clients():
    conn = get_connection()
    clients = conn.execute("SELECT * FROM client").fetchall()
    conn.close()
    return jsonify([dict(row) for row in clients])

#================================
# Login employee Mobile
#================================

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM employe WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        return jsonify({
            "success": True,
            "employe_id": user["id"]
        })
    else:
        return jsonify({"success": False}), 401


# ==============================
#  LISTER LES SERVICE FAIT
# ==============================
@app.route('/servicefait', methods=['GET'])
def get_service_fait():
    conn = get_connection()
    rows = conn.execute("""
        SELECT sf.id,
               c.nom,
               sf.commentaire,
               sf.total,
               sf.date
        FROM service_fait sf
        LEFT JOIN client c ON sf.client_id = c.id
        ORDER BY sf.date DESC
    """).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5602, debug=True)