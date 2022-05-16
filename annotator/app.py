import database

from flask import Flask, send_from_directory, render_template, request

db = database.Connection()
app = Flask(__name__)


@app.route("/")
def index():
    post = get_random_row()
    return render_template("index.html", post=post)


@app.route("/login")
def login():
    return render_template("login.html")


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


@app.route("/top/<subreddit>")
def top(subreddit):
    t = db.get_top_for_subreddit(subreddit, 100)
    top = []
    for p in t:
        post = p
        post["text"] = post["text"].replace("\n", "<br>")
        top.append(post)
    return render_template("top.html", top=top)


@app.route("/polls/<subreddit>")
def polls(subreddit):
    t = db.get_polls_of_subreddit(subreddit, 100)
    polls = []
    for p in t:
        post = p
        post["text"] = post["text"].replace("\n", "<br>")
        polls.append(post)
    return render_template("polls.html", polls=polls)
# 
@app.route("/min/<subreddit>")
def min(subreddit):
    t = db.get_min_from_subreddit(subreddit, 100)
    min = []
    for p in t:
        post = p
        post["text"] = post["text"].replace("\n", "<br>")
        min.append(post)
    return render_template("min.html", min=min)

@app.route("/get-random-row")
def get_random_row():
    post = db.select_random_unannotated_post()
    post["text"] = post["text"].replace("\n", "<br>")
    return post


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
