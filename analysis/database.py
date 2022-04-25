# Module Imports
from ctypes.wintypes import HACCEL
import mariadb
import sys
import json
import os

from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
HOST = os.getenv("DATABASE_HOST")
PORT = int(os.getenv("DATABASE_PORT"))
NAME = os.getenv("DATABASE_NAME")

TABLES = ["unannotated_posts", "annotator", "annotations"]
INIT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
INIT_DIRECTORY = INIT_DIRECTORY + "/../initialization"


class Connection:
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database=NAME,
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.init_tables()

    def init_tables(self):
        self.tables = {}
        for table_name in TABLES:
            self.tables[table_name] = self.import_columns(table_name)

    def import_columns(self, table_name):
        try:
            file = open(f"{INIT_DIRECTORY}/json/{table_name}.json")
            return [column for column, meta_data in json.load(file)["COLUMNS"].items()]
        except:
            print(f"Failed to open: {INIT_DIRECTORY}/json/{table_name}.json")
            return []

    def get_all_annotations(self):
        pass
    
    def get_all_annotations__after_before(self):
        pass