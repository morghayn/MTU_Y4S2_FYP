from flask import Flask, send_from_directory, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/styles.css")
def styles():
    return send_from_directory("static/css", "styles.css")


@app.route("/script.js")
def scripts():
    return send_from_directory("static/js", "script.js")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
