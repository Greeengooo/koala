from sqlalchemy.exc import ProgrammingError


class Fetcher:
    def __init__(self, current_connection):
        self.connection = current_connection

    def fetch_data(self, sql_query):
        try:
            results = self.connection.execute(sql_query)
            if "USE" not in sql_query.split(" "):
                return {"status": "RAN", "data": results.fetchall()}
        except ProgrammingError as err:
            print(err)
            return {"status": "FAILED", "data": err.args}