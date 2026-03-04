from flask import Flask, render_template, request, redirect, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "secret_key"

AUTH_URL = "http://127.0.0.1:5400"
INCIDENT_URL = "http://127.0.0.1:5000/incidents"
ABSENCE_URL = "http://127.0.0.1:5100/absences"
SERVICE_FAIT_URL = "http://127.0.0.1:5300/servicefait"

@app.route("/")
def home():
    return render_template("login.html", error=False)


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    try:
        response = requests.post(
            f"{AUTH_URL}/login",
            json={
                "username": username,
                "password": password
            }
        )

        if response.headers.get("Content-Type", "").startswith("application/json"):
            data = response.json()
        else:
            return render_template("login.html", error=True)

        if response.status_code == 200 and data.get("success") and "token" in data:
            session["token"] = data["token"]
            return redirect("/dashboard")

    except Exception as e:
        print("AUTH ERROR:", e)

    return render_template("login.html", error=True)

@app.route("/dashboard")
def admin_dashboard():
    incidents = requests.get(INCIDENT_URL).json()["data"]
    absences = requests.get(ABSENCE_URL).json()["data"]
    services_fait = requests.get(SERVICE_FAIT_URL).json()

    return render_template(
        "admin_dashboard.html",
        incidents=incidents,
        absences=absences,
        services_fait = services_fait
    )


@app.route("/logout")
def logout():
    session.pop("token", None)
    return redirect("/")

# =======================================
# UPDATE STATUT - PROXY vers SRV INCIDENT
# =======================================
@app.route("/incidents/<int:id>/statut", methods=["POST"])
def update_statut(id):
    data = request.get_json()

    # Forward vers le service incident
    r = requests.post(f"{INCIDENT_URL}/{id}/statut", json=data)

    return jsonify(r.json()), r.status_code



if __name__ == "__main__":
    app.run(port=7000, debug=True)