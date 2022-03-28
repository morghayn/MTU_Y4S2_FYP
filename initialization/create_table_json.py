import json


def unannotated_posts():
    unannotated_posts = {
        "author_id": {
            "datatype": "VARCHAR",
            "size": 10,
            "rules": "",
        },
        "author_name": {
            "datatype": "VARCHAR",
            "size": 20,
            "rules": "",
        },
        "subreddit_id": {
            "datatype": "VARCHAR",
            "size": 10,
            "rules": "",
        },
        "subreddit_display_name": {
            "datatype": "VARCHAR",
            "size": 20,
            "rules": "",
        },
        "creation_time_utc": {
            "datatype": "DOUBLE",
            "size": "20,5",
            "rules": "",
        },
        # "edited": {
        #     "datatype": "BOOLEAN",
        #     "rules": "",
        # },
        "ticker_list": {
            "datatype": "TEXT",
            "rules": "",
        },
        "id": {
            "datatype": "VARCHAR",
            "size": 10,
            "rules": "",
        },
        "name": {
            "datatype": "VARCHAR",
            "size": 10,
            "rules": "",
        },
        "title": {
            "datatype": "VARCHAR",
            "size": 300,
            "rules": "",
        },
        "text": {
            "datatype": "TEXT",
            "rules": "",
        },
        "upvote_ratio": {
            "datatype": "DOUBLE",
            "size": "10,5",
            "rules": "",
        },
        "score": {
            "datatype": "INT",
            "rules": "",
        },
        "num_of_comments": {
            "datatype": "INT",
            "rules": "",
        },
        "stickied": {
            "datatype": "BOOLEAN",
            "rules": "",
        },
        "locked": {
            "datatype": "BOOLEAN",
            "rules": "",
        },
        "over_18": {
            "datatype": "BOOLEAN",
            "rules": "",
        },
        "spoiler": {
            "datatype": "BOOLEAN",
            "rules": "",
        },
        "url": {
            "datatype": "VARCHAR",
            "size": 700,
            "rules": "",
        },
    }

    with open("unannotated_posts.json", "w") as write_file:
        json.dump(unannotated_posts, write_file, indent=4)


unannotated_posts()
