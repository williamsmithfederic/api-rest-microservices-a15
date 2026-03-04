from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def bi_dashboard():
    return render_template("bi_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
