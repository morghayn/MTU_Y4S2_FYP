# Module Imports
from ctypes.wintypes import HACCEL
from dotenv import load_dotenv
from contextlib import closing
import create_query
import mariadb
import sys
import json
import os


load_dotenv()

USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
HOST = os.getenv("DATABASE_HOST")
PORT = int(os.getenv("DATABASE_PORT"))
NAME = os.getenv("DATABASE_NAME")

TABLES = ["unannotated_posts", "annotator", "annotations"]
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class Connection:
    def __init__(self) -> None:
        print(USER, "*" * len(PASSWORD), HOST, PORT, NAME)
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
            file = open(f"{CURRENT_DIRECTORY}/json/{table_name}.json")
            return [column for column, meta_data in json.load(file)["COLUMNS"].items()]
        except:
            print(f"Failed to open: {CURRENT_DIRECTORY}/json/{table_name}.json")
            return []

    def insert_row(self, table_name, data, notify=False):
        columns = self.tables[table_name]
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    f"INSERT INTO {table_name} ({','.join([str(x) for x in columns])})"
                    + f" VALUES ({','.join(['?' for x in columns])})",
                    tuple([data[i] for i in range(0, len(columns))]),
                )
                self.conn.commit()
            if notify:
                print("Sucessfully inserted row.")
        except mariadb.Error as e:
            # print(f"Could not insert row: {e}")
            pass

    def retrieve_all(self, table_name):
        try:
            with closing(self.conn.cursor()) as cursor:
                statement = f"SELECT * FROM {table_name}"
                cursor.execute(statement)
                for row in cursor:
                    print(row)
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")

    def retrieve_random_row(self, table_name):
        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"SELECT * FROM {table_name} ORDER BY RAND() LIMIT 1"
                dict_cursor.execute(statement)
                dictionary = dict_cursor.fetchone()
                return dictionary
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")

    def drop_table(self, table_name):
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute("DROP TABLE " + table_name)
                print(f"Successfully dropped table '{table_name}'.")
        except mariadb.Error as e:
            print(f"Could not drop table: {e}")

    def create_table(self, table_name, primary_key_name="id"):
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(create_query.compile(table_name, primary_key_name))
                print(f"Successfully created table '{table_name}'.")
        except mariadb.Error as e:
            print(f"Could not create table: {e}")

    def get_columns_list(self, table_name):
        # TODO: Check if table_name exists...
        return self.tables[table_name]
