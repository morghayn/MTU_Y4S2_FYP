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
            file = open(f"{INIT_DIRECTORY}/json/{table_name}.json")
            return [column for column, meta_data in json.load(file)["COLUMNS"].items()]
        except:
            print(f"Failed to open: {INIT_DIRECTORY}/json/{table_name}.json")
            return []

    def count_unannotated(self, after, before, subreddit):
        res = []

        try:
            with closing(self.conn.cursor()) as cursor:
                statement = f"""
                    SELECT 
                        COUNT(*)
                    FROM
                        unannotated_posts
                    WHERE
                        creation_time_utc > {after}
                    AND
                        creation_time_utc < {before}
                    AND
                        subreddit_display_name = \"{subreddit}\"
                """
                cursor.execute(statement)
                res = cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res[0]

    def get_all_ticker_lists(self):
        res = []

        try:
            with closing(self.conn.cursor()) as cursor:
                statement = f"""
                    SELECT 
                        ticker_list
                    FROM
                        unannotated_posts
                """
                cursor.execute(statement)
                res = cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def get_spys_average_sentiment_for_month(self, annotator_id, before, after):
        """
        to do this we are just getting the average sentiment among all annotations made by annotator of id give in parameters
        """
        try:
            with closing(self.conn.cursor()) as cursor:
                statement = f"""
                    SELECT
                        AVG(annotations.sentiment) as average
                    FROM
                        unannotated_posts
                    RIGHT JOIN annotations
                        ON unannotated_posts.id = annotations.post_id
                    WHERE
                        annotations.annotator_id = {annotator_id}
                    AND
                        unannotated_posts.creation_time_utc > {after}
                    AND 
                        unannotated_posts.creation_time_utc < {before};    
                """
                cursor.execute(statement)
                res = float(cursor.fetchone()[0])
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res

    def get_average_sentiment_for_unknown_ticker_for_period_before_after(
        self, annotator_id, before, after, ticker
    ):
        """
        to do this we are just getting the average sentiment among all annotations made by annotator of id give in parameters
        """
        res = 0

        try:
            with closing(self.conn.cursor()) as cursor:
                statement = f"""
                    SELECT
                        AVG(annotations.sentiment) as average
                    FROM
                        unannotated_posts
                    RIGHT JOIN annotations
                        ON unannotated_posts.id = annotations.post_id
                    WHERE
                        annotations.annotator_id = {annotator_id}
                    AND
                        unannotated_posts.creation_time_utc > {after}
                    AND 
                        unannotated_posts.creation_time_utc < {before}
                    AND
                        unannotated_posts.ticker_list like \"%{ticker}%\";
                """
                cursor.execute(statement)
                res = float(cursor.fetchone()[0])
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return res
