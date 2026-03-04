from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "incidents.db")


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"success": False}), 400

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM employe WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    conn.close()

    if user:
        return jsonify({
            "success": True,
            "employe_id": user["id"]
        }), 200

    return jsonify({"success": False}), 401


if __name__ == "__main__":
    app.run(port=5603, debug=True)