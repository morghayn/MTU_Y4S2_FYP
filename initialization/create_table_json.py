import json
import os


CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = "json"


def unannotated_posts():
    unannotated_posts = {
        "COLUMNS": {
            #
            # Identifiers
            #
            "author_id": {
                "datatype": "VARCHAR",
                "size": 10,
                "constraints": "",
            },
            "author_name": {
                "datatype": "VARCHAR",
                "size": 20,
                "constraints": "",
            },
            "subreddit_id": {
                "datatype": "VARCHAR",
                "size": 10,
                "constraints": "",
            },
            "subreddit_display_name": {
                "datatype": "VARCHAR",
                "size": 20,
                "constraints": "",
            },
            "id": {
                "datatype": "VARCHAR",
                "size": 10,
                "constraints": "",
            },
            #
            # Important Meta Data
            #
            "creation_time_utc": {
                "datatype": "DOUBLE",
                "size": "20,5",
                "constraints": "",
            },
            "name": {
                "datatype": "VARCHAR",
                "size": 10,
                "constraints": "",
            },
            "title": {
                "datatype": "VARCHAR",
                "size": 300,
                "constraints": "",
            },
            "ticker_list": {
                "datatype": "TEXT",
                "constraints": "",
            },
            "text": {
                "datatype": "TEXT",
                "constraints": "",
            },
            "upvote_ratio": {
                "datatype": "DOUBLE",
                "size": "10,5",
                "constraints": "",
            },
            "score": {
                "datatype": "INT",
                "constraints": "",
            },
            "num_of_comments": {
                "datatype": "INT",
                "constraints": "",
            },
            #
            # Less Important Meta Data
            #
            "edited": {
                "datatype": "BOOLEAN",
                "constraints": "",
            },
            "stickied": {
                "datatype": "BOOLEAN",
                "constraints": "",
            },
            "locked": {
                "datatype": "BOOLEAN",
                "constraints": "",
            },
            "over_18": {
                "datatype": "BOOLEAN",
                "constraints": "",
            },
            "spoiler": {
                "datatype": "BOOLEAN",
                "constraints": "",
            },
            #
            # Quick Access
            #
            "url": {
                "datatype": "VARCHAR",
                "size": 700,
                "constraints": "",
            },
        },
        "PRIMARY_KEYS": ["id"],
    }

    with open(f"{CURRENT_DIRECTORY}/{OUTPUT_DIR}/unannotated_posts.json", "w") as write_file:
        json.dump(unannotated_posts, write_file, indent=4)


def create_save_folder_if_not_exist():
    if not os.path.exists(f"{CURRENT_DIRECTORY}/{OUTPUT_DIR}/"):
        os.makedirs(f"{CURRENT_DIRECTORY}/{OUTPUT_DIR}/")


def export(table_name):
    if table_name == "unannotated_posts":
        print(f"Exporting {table_name}")
        unannotated_posts()
