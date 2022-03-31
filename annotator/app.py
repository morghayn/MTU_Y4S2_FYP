from flask import Flask, send_from_directory, render_template, request


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
    data = {
        "id": "success-1",
        "title": "success-2",
        "ticker_list": "success-3",
        "subreddit_display_name": "success-4",
        "author_name": "success-5",
        "url": '<a href="/#" target="blank_">success-6</a>',
        "text": "success",
    }
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
