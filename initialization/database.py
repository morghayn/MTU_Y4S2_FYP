# Module Imports
from ctypes.wintypes import HACCEL
from dotenv import load_dotenv
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

TABLES = ["unannotated_posts"]

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

        self.dict_cursor = self.conn.cursor(dictionary=True)
        self.cursor = self.conn.cursor()
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

    def insert_row(self, table_name, data):
        columns = self.tables[table_name]
        try:
            self.cursor.execute(
                f"INSERT INTO {table_name} ({','.join([str(x) for x in columns])})"
                + f" VALUES ({','.join(['?' for x in columns])})",
                tuple([data[i] for i in range(0, len(columns))]),
            )
            self.conn.commit()
            print("Sucessfully inserted row.")
        except mariadb.Error as e:
            print(f"Could not insert row: {e}")
            # print(tuple([data[i] for i in range(0, len(columns))])) # For debug purposes

    def retrieve_all(self, table_name):
        try:
            statement = f"SELECT * FROM {table_name}"
            self.cursor.execute(statement)
            for row in self.cursor:
                print(row)
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")

    def retrieve_random_row(self, table_name):
        try:
            statement = f"SELECT * FROM {table_name} ORDER BY RAND() LIMIT 1"
            self.dict_cursor.execute(statement)
            dictionary = self.dict_cursor.fetchone()
            return dictionary

        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")

    def drop_table(self, table_name):
        try:
            self.cursor.execute("DROP TABLE " + table_name)
            print(f"Successfully dropped table '{table_name}'.")
        except mariadb.Error as e:
            print(f"Could not drop table: {e}")

    def create_table(self, table_name, primary_key_name="id"):
        try:
            self.cursor.execute(create_query.compile(table_name, primary_key_name))
            self.cursor.execute(
                f"ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin"
            )
            print(f"Successfully created table '{table_name}'.")
        except mariadb.Error as e:
            print(f"Could not create table: {e}")

    def get_columns_list(self, table_name):
        """
        Used to return list of all columns for specific table in database.
        """
        # TODO: Check if table_name exists...
        return self.tables[table_name]
