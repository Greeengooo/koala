import os.path
import sqlite3
from sqlite3 import Error

from internal_storage.config import CREATE_CONNECTION_TABLE, DATABASE_NAME, CREATE_RESULTS_TABLE


class Storage:
    def __init__(self):
        self.connection = None
        self.create_or_connect()

    def create_or_connect(self):
        if not os.path.isfile(DATABASE_NAME):
            connection = sqlite3.connect(DATABASE_NAME)
            self.execute_query(CREATE_CONNECTION_TABLE)
            self.execute_query(CREATE_RESULTS_TABLE)
        else:
            self.connection = sqlite3.connect(DATABASE_NAME)

    def execute_query(self, query, args=tuple()):
        try:
            connection = sqlite3.connect(DATABASE_NAME)
            cursor = connection.cursor()
            query_results = cursor.execute(query, args).fetchall()
        except Error as err:
            return {"status": "FAILED", "result": err.args}

        connection.commit()
        return {"status": "SUCCESS", "result": query_results}
