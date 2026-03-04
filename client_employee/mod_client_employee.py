from flask import Flask, render_template, request, redirect, url_for
import requests


app = Flask(__name__)


SRV_INCIDENT_URL = "http://127.0.0.1:5000/incidents"
SRV_ABSENCE_URL = "http://127.0.0.1:5100/absences"



# =========================
# HOME employee
# =========================

@app.route("/")
def home():
    from flask import url_for
    return redirect(url_for("login"))

@app.route("/employee")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def employee_dashboard():
    return render_template("employee_dashboard.html")

@app.route("/logout")
def logout():
    return render_template("login.html")

# =========================
# INCIDENT
# =========================
@app.route("/incident")
def incident_form():
    return render_template("incident_form.html")

@app.route("/envoyer_incident", methods=["POST"])
def envoyer_incident():
    data = {
        "nom": request.form["nom"],
        "prenom": request.form["prenom"],
        "type_incident": request.form["type_incident"],
        "priorite": request.form["priorite"],
        "description": request.form["description"]
    }
    requests.post(SRV_INCIDENT_URL, json=data)
    return redirect(url_for("employee_dashboard"))


# =========================
# ABSENCE
# =========================
@app.route("/absence")
def absence_form():
    return render_template("absence_form.html")

@app.route("/envoyer_absence", methods=["POST"])
def envoyer_absence():
    data = {
        "nom": request.form["nom"],
        "prenom": request.form["prenom"],
        "type_absence": request.form["type_absence"],
        "date_debut": request.form["date_debut"],
        "date_fin": request.form["date_fin"],
        "description": request.form["description"]
    }
    requests.post(SRV_ABSENCE_URL, json=data)
    return redirect(url_for("employee_dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=4000)
