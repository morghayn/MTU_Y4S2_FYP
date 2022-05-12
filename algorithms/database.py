# Module Imports
from ctypes.wintypes import HACCEL
from contextlib import closing
from dotenv import load_dotenv
import pandas as pd
import warnings
import mariadb
import sys
import os

# Ignoring user warning that pandas.read_sql_query is running
warnings.simplefilter(action="ignore", category=UserWarning)

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

    def select__from__by__(self, columns, annotator):
        """
        Will return DataFrame of specified columns from unannotated_posts
        where an annotation has been provided in annotations
        by the annotator specified by their username
        """
        df = pd.DataFrame()

        try:
            statement = f"""
                SELECT
                    {",".join([str(x) for x in columns])}
                FROM 
                    unannotated_posts AS up
                INNER JOIN 
                    annotations as a
                ON
                    up.id = a.post_id
                WHERE
                    annotator_id = (
                        SELECT
                            id
                        FROM
                            annotator
                        WHERE
                            username like "%{annotator}%"
                        LIMIT
                            1
                    );
                """
            # This is giving an error, but it is also working, so I guess we will proceed with caution?
            df = pd.read_sql(statement, self.conn)
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
        finally:
            return df
