import json
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = "json"
TABLES = ["unannotated_posts", "annotator", "annotations"]


def create_save_folder_if_not_exist():
    if not os.path.exists(f"{CURRENT_DIRECTORY}/{OUTPUT_DIR}/"):
        os.makedirs(f"{CURRENT_DIRECTORY}/{OUTPUT_DIR}/")


def get_dictionary(table):
    """
    Switch statement to return corresponding dictionary to table_name string passed
    """
    res = {}

    if table == "unannotated_posts":
        res = UNANNOATED_POSTS
    elif table == "annotator":
        res = ANNOTATOR
    elif table == "annotations":
        res = ANNOTATIONS

    return res


def export_all():
    create_save_folder_if_not_exist()
    for table in TABLES:
        print(f"Exporting {table}")
        with open(f"{CURRENT_DIRECTORY}/{OUTPUT_DIR}/{table}.json", "w") as write_file:
            json.dump(get_dictionary(table), write_file, indent=4)


def compile(table_name, primary_key_name):
    with open(f"{CURRENT_DIRECTORY}/json/{table_name}.json") as json_file:
        table = json.load(json_file)

    query = f"CREATE TABLE {table_name}\n(\n"
    for field, values in table["COLUMNS"].items():
        size = "" if "size" not in values else f"({str(values['size'])})"
        datatype = values["datatype"]
        constraints = values["constraints"]
        if constraints:
            constraints = " " + constraints
        #
        query += f"\t{field} {datatype}{size}{constraints},\n"

    # Primary key
    keys = table["PRIMARY_KEYS"]
    query += f"\tCONSTRAINT {primary_key_name} PRIMARY KEY ({','.join([str(key) for key in keys])})"

    # If foreign keys
    if "FOREIGN_KEYS" in table:
        query += ",\n"
        foreign_keys = table["FOREIGN_KEYS"]
        for i, (key, value) in enumerate(foreign_keys.items()):
            query += f"\tCONSTRAINT FOREIGN KEY(`{key}`)"
            query += f"\n\t\tREFERENCES `{value['TABLE']}` (`{value['FIELD']}`)"
            for option in value['OPTIONS']:
                query += f"\n\t\t{option}"
            query += "\n" if i == (len(foreign_keys) - 1) else ",\n"
        
    else:
        query += "\n"

    # Closing
    query += ")\n"
    query += "CHARACTER SET utf8mb4\n"
    query += "COLLATE utf8mb4_bin\n"

    # print(f"{table_name}\n{query}\n\n")
    return query


UNANNOATED_POSTS = {
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
            "datatype": "DOUBLE",
            "size": "20,5",
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

ANNOTATOR = {
    "COLUMNS": {
        "id": {
            "datatype": "INT",
            "constraints": "NOT NULL AUTO_INCREMENT",
        },
        "username": {
            "datatype": "VARCHAR",
            "size": 255,
            "constraints": "",
        },
    },
    "PRIMARY_KEYS": ["id"],
}

ANNOTATIONS = {
    "COLUMNS": {
        "id": {
            "datatype": "INT",
            "constraints": "AUTO_INCREMENT",
        },
        "post_id": {
            "datatype": "VARCHAR",
            "size": 10,
            "constraints": "",
        },
        "annotator_id": {
            "datatype": "INT",
            "constraints": "",
        },
        "sentiment": {
            "datatype": "TINYINT",
            "constraints": "",
        },
        "insertion_timestamp": {
            "datatype": "DOUBLE",
            "size": "20,5",
            "constraints": "",
        },
    },
    "PRIMARY_KEYS": ["id"],
    "FOREIGN_KEYS": {
        "post_id": {
            "TABLE": "unannotated_posts",
            "FIELD": "id",
            "OPTIONS": ["ON DELETE CASCADE", "ON UPDATE CASCADE"],
        },
        "annotator_id": {
            "TABLE": "annotator",
            "FIELD": "id",
            "OPTIONS": ["ON DELETE CASCADE", "ON UPDATE CASCADE"],
        },
    },
}
