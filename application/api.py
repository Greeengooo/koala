import pandas
from entities import fetcher
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from models import Connection, CredentialsDB, Query
from starlette.staticfiles import StaticFiles

from application.entities import query
from application.entities.connector import Connector
from application.entities.data_resource_info import DataResourceInfo
from application.render_main import create_template

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "DELETE"],
)

connector = Connector()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return create_template('mainH.html', request, connector)


@app.post("/connect")
async def handle_connect(credentials: CredentialsDB):
    try:
        connection_response = connector.connect(credentials)
        connection_status = connection_response["status"]
        return {"status": connection_status, "connection": credentials.db_name}
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Failed to connect: {err}")


@app.post("/select")
async def select_connection(connection: Connection):
    connector.select_connection(connection.connection)
    return f"Selected {connection.connection}"


@app.get("/data-source-info", status_code=201, summary="Retrive all the information about data source databases")
def get_info():
    return DataResourceInfo(connector.current_connection).fetch_all_info()


@app.get("/connected", status_code=201, summary="Get connected databases")
async def list_connected_dbs():
    return connector.get_all_connections()


@app.get(
    "/connected/{connection_id}", status_code=201, summary="Get specific connection"
)
async def get_connection(connection_id):
    return connector.get_connection(connection_id)

@app.delete(
    "/delete/{connection_id}", status_code=201, summary="Delete specific connection"
)
async def delete_connection_by_id(connection_id):
    return connector.delete_connection_by_id(connection_id)


@app.delete("/delete", status_code=201, summary="Delete all connections")
async def delete_all_connections():
    return connector.delete_all_connections()


@app.post("/compile", status_code=201, summary="Run logica query")
def run_query(q: Query):
    query_sql = query.compile_to_sql(connector.current_engine, q)
    compilations_status = query_sql["status"]
    sql = query_sql["sql"]
    if compilations_status == "FAILED":
        raise HTTPException(status_code=404, detail=sql)

    results = fetcher.Fetcher(connector.current_connection).fetch_data(sql)
    sql_status = results["status"]
    data = results["data"]
    if sql_status == "FAILED":
        raise HTTPException(status_code=404, detail=data)

    df_result = pandas.DataFrame(data)
    html = df_result.to_html()
    row_count = len(df_result)
    return {"html": html, "row_count": str(row_count)}