DATABASE_NAME = "../internal_storage/connection.db"

CREATE_CONNECTION_TABLE = """CREATE TABLE CONNECTION (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                db_name VARCHAR NOT NULL,
                                connection_obj VARCHAR NOT NULL,
                                UNIQUE(connection_obj));"""

CREATE_RESULTS_TABLE = """ CREATE TABLE RESULTS (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            result VARCHAR NOT NULL); """

RESET_AUTO_INCREMENT = (
    """UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'CONNECTION';"""
)

INSERT_CONNECTION = """INSERT INTO CONNECTION (db_name, connection_obj)
                       VALUES (?, ?)"""

GET_ALL_CONNECTIONS = """SELECT id, db_name,connection_obj FROM CONNECTION"""

GET_SPECIFIC_CONNECTION = """SELECT * FROM CONNECTION WHERE db_name == ?"""

DELETE_ALL_CONNECTIONS = """DELETE FROM CONNECTION"""

DELETE_SPECIFIC_CONNECTION = """DELETE FROM CONNECTION WHERE id == ?"""