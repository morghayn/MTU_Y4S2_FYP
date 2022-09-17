# Module Imports
from ctypes.wintypes import HACCEL
from dotenv import load_dotenv
from contextlib import closing
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

    def select_random_unannotated_post(self, username, minimum_upvotes):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"""
                    SELECT 
                        *
                    FROM 
                        unannotated_posts 
                    WHERE 
                        id NOT IN (
                            SELECT 
                            post_id
                        FROM
                            annotations
                        WHERE
                            annotator_id = (
                                SELECT
                                    id
                                FROM
                                    annotator
                                WHERE
                                    username = "{username}"
                                )
                            )
                    AND
                        score > {minimum_upvotes}
                    ORDER BY 
                        RAND()
                    LIMIT 
                        1
                """
                dict_cursor.execute(statement)
                res = dict_cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def select_all_posts(self):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = "SELECT * FROM unannotated_posts"
                dict_cursor.execute(statement)
                res = dict_cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def select_all_posts__with_greater_than_x_upvotes(self, x):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"SELECT * FROM unannotated_posts WHERE score > {x}"
                dict_cursor.execute(statement)
                res = dict_cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def get_annotator_id(self, username):
        res = None

        try:
            with closing(self.conn.cursor()) as cursor:
                statement = f'SELECT id FROM annotator WHERE username = "{username}"'
                cursor.execute(statement)
                res = cursor.fetchone()[0]
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def insert(self, table_name, data, auto_increment=False, notify=False):
        columns = self.tables[table_name]
        if auto_increment and "id" in columns:
            columns.remove("id")

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
            print(f"Could not insert row: {e}")

    """
    Functions that are currently not utilized/in-use.
    """
    def select_post_by_id(self, id):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"""
                    SELECT 
                        *
                    FROM 
                        unannotated_posts 
                    WHERE 
                        id = "{id}"
                    LIMIT 
                        1
                """
                dict_cursor.execute(statement)
                res = dict_cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res