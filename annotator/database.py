# Module Imports
from ctypes.wintypes import HACCEL
from dotenv import load_dotenv
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

        self.dict_cursor = self.conn.cursor(dictionary=True)
        self.cursor = self.conn.cursor()

    def select_random_unannotated_post(self):
        res = {}

        try:
            statement = "SELECT * FROM unannotated_posts ORDER BY RAND() LIMIT 1"
            self.dict_cursor.execute(statement)
            res = self.dict_cursor.fetchone()

        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        
        finally:
            return res
