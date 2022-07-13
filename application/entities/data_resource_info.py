from application.entities.fetcher import Fetcher

MYSQL_FIELDS = {"database_name": "Database", "table_name": "Tables_in_{database}"}
SNOWFLAKE_FIELDS = {"database_name": "name", "table_name": "name"}


class DataResourceInfo:
    def __init__(self, current_connection):
        self.connection = current_connection
        self.db_name = current_connection.engine.name

    def fetch_all_info(self):
        all_info = {}
        database_field, table_field = self.get_fields()
        db_info = self.fetch_db_info()
        for db in db_info:
            db_name = db[database_field]
            table_info = self.fetch_table_info(db_name)
            all_info[db_name] = list(map(lambda x: x[table_field.format(database=db_name)], table_info))
        return all_info

    def get_fields(self):
        if self.db_name == "snowflake":
            return SNOWFLAKE_FIELDS["database_name"], SNOWFLAKE_FIELDS["table_name"]
        elif self.db_name == "mysql":
            return MYSQL_FIELDS["database_name"], MYSQL_FIELDS["table_name"]

    def fetch_db_info(self):
        return Fetcher(self.connection).fetch_data("SHOW DATABASES;")["data"]

    def fetch_table_info(self, db):
        fetcher = Fetcher(self.connection)
        fetcher.fetch_data(f"USE {db};")
        return fetcher.fetch_data("SHOW TABLES")["data"]