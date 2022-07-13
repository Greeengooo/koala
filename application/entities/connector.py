import json

from sqlalchemy import create_engine

from application.models import CredentialsDB
from internal_storage.config import (DELETE_ALL_CONNECTIONS,
                                     DELETE_SPECIFIC_CONNECTION,
                                     GET_ALL_CONNECTIONS,
                                     GET_SPECIFIC_CONNECTION,
                                     INSERT_CONNECTION, RESET_AUTO_INCREMENT)
from internal_storage.storage import Storage
from application.entities.encryptor import EncryptorService


class Connector:
    def __init__(self):
        self.connection_credentials = None
        self.storage = Storage()
        self.current_connection = None
        self.current_engine = None
        self.connection_pool = {}

    def connect(self, connection_credentials):
        self.connection_credentials = connection_credentials
        url = self.form_connection_url()
        engine = create_engine(url)
        connection = engine.connect()
        self.connection_pool[self.connection_credentials.db_name] = connection_credentials
        self.current_connection = connection
        self.current_engine = connection_credentials.db_name
        connection_credentials.password = EncryptorService().encode(connection_credentials.password)
        return self.save_connection(
            self.connection_credentials.db_name, connection_credentials.json()
        )

    def select_connection(self, connection):
        connection_credentials = self.get_connection(connection)["result"]["connection_obj"]
        connection_credentials.password = EncryptorService().decode(connection_credentials.password)
        self.connection_credentials = connection_credentials
        url = self.form_connection_url()
        engine = create_engine(url)
        connection = engine.connect()
        self.current_connection = connection
        self.current_engine = self.connection_credentials.db_name

    def form_connection_url(self):
        if self.connection_credentials.db_name == "snowflake":
            url_template = "snowflake://{user}:{password}@{account_identifier}/"
            return url_template.format(
                user=self.connection_credentials.username,
                password=self.connection_credentials.password,
                account_identifier=self.connection_credentials.account_identifier,
            )
        elif self.connection_credentials.db_name == "mysql":
            url_template = "mysql+pymysql://{user}:{password}@localhost/"
            return url_template.format(
                user=self.connection_credentials.username,
                password=self.connection_credentials.password)
        else:
            raise Exception(f"{self.connection_credentials.db_name} in not supported")

    def delete_all_connections(self):
        self.storage.execute_query(RESET_AUTO_INCREMENT)
        return self.storage.execute_query(DELETE_ALL_CONNECTIONS)

    def delete_connection_by_id(self, connection_id):
        response = self.get_connection(connection_id)
        self.storage.execute_query(DELETE_SPECIFIC_CONNECTION, args=(connection_id,))
        return self.form_response_dict(status="SUCCESS", result=response["result"])

    def get_connection(self, connection_name):
        sqlite_response = self.storage.execute_query(
            GET_SPECIFIC_CONNECTION, args=(connection_name,)
        )
        if len(sqlite_response["result"]) == 0:
            return self.form_response_dict(
                status="FAILED",
                result=f"Connection with name == {connection_name} not found",
            )

        conn_id, db_name, metadata = sqlite_response["result"][0]
        connection_obj = self.form_connection_obj(json.loads(metadata))
        return self.form_response_dict(
            status="SUCCESS",
            result={"id": conn_id, "db_name": db_name, "connection_obj": connection_obj},
        )

    def get_all_connections(self):
        self.storage.create_or_connect()
        sqlite_response = self.storage.execute_query(GET_ALL_CONNECTIONS)
        all_connections = []
        for connection in sqlite_response["result"]:
            conn_id, db_name, metadata = connection
            all_connections.append(
                {"id": conn_id, "db_name": db_name, "metadata": metadata}
            )
        return all_connections

    def save_connection(self, db_name, connection: str):
        exists = self.storage.execute_query("SELECT db_name FROM CONNECTION WHERE db_name == ?", args=(db_name,))
        if len(exists["result"]) == 0:
            sqlite_response = self.storage.execute_query(
                INSERT_CONNECTION, args=(db_name, connection)
            )
        else:
           raise Exception("Already connected")

        if sqlite_response["status"] == "FAILED":
            return self.form_response_dict(
                status="FAILED", result=sqlite_response["result"]
            )
        else:
            return self.form_response_dict(
                status="SUCCESS", result={db_name: connection}
            )

    def form_connection_obj(self, metadata):
        return CredentialsDB(**metadata)

    def form_response_dict(self, status, result):
        return {"status": status, "result": result}
