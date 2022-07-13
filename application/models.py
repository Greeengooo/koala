from typing import Optional

from pydantic import BaseModel


class CredentialsDB(BaseModel):
    db_name: str
    username: str
    password: str
    account_identifier: str = None


class Query(BaseModel):
    predicate: str
    query_text: str


class Connection(BaseModel):
    connection: str