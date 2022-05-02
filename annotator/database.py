# Module Imports
from ctypes.wintypes import HACCEL
from dotenv import load_dotenv
from contextlib import closing
import mariadb
import sys
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

    def select_random_unannotated_post(self):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"""
                    SELECT 
                        * 
                    FROM 
                        unannotated_posts 
                    ORDER BY 
                        RAND() 
                    LIMIT 1
                """
                dict_cursor.execute(statement)
                res = dict_cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def get_top_for_subreddit(self, subreddit, limit):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"""
                    SELECT 
                        * 
                    FROM 
                        unannotated_posts 
                    WHERE 
                        subreddit_display_name = "{subreddit}" 
                    ORDER BY 
                        (CHAR_LENGTH(title) + CHAR_LENGTH(text)) 
                    DESC 
                    LIMIT 
                        {limit}
                """
                dict_cursor.execute(statement)
                res = dict_cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def get_min_from_subreddit(self, subreddit, limit):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"""
                    SELECT 
                        * 
                    FROM 
                        unannotated_posts 
                    WHERE 
                        subreddit_display_name = "{subreddit}" 
                    AND 
                        score > 20 
                    ORDER BY 
                        (CHAR_LENGTH(title) + CHAR_LENGTH(text)) 
                    DESC 
                    LIMIT 
                        {limit}
                """
                dict_cursor.execute(statement)
                res = dict_cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def get_polls_of_subreddit(self, subreddit, limit):
        res = {}

        try:
            with closing(self.conn.cursor(dictionary=True)) as dict_cursor:
                statement = f"""
                    SELECT 
                        * 
                    FROM 
                        unannotated_posts 
                    WHERE 
                        text like "%[View Poll]%" 
                    LIMIT 
                        {limit}
                """
                dict_cursor.execute(statement)
                res = dict_cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res
