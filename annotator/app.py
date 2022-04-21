import database

from flask import Flask, send_from_directory, render_template, request

db = database.Connection()
app = Flask(__name__)


@app.route("/")
def index():
    post = get_random_row()
    return render_template("index.html", post=post)


@app.route("/styles.css")
def styles():
    return send_from_directory("static/css", "styles.css")


@app.route("/script.js")
def scripts():
    return send_from_directory("static/js", "script.js")


@app.route("/process-evaluation", methods=["POST"])
def process_evaluation():
    data = request.get_json()
    id = data["id"]
    annotation = data["annotation"]
    print("id:", id)
    print("annotation:", annotation)
    #
    # TODO: Process evaluation
    #
    return ("", 204)


@app.route("/get-random-row")
def get_random_row():
    post = db.select_random_unannotated_post()
    post['text'] = post['text'].replace('\n', '<br>')
    return post


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
