import requests


def test_connection():
    connection_obj = {"db_name": "snowflake", "username": "aanoshyn", "password": "", "account_identifier": "zjb39083.us-east-1"}
    response = requests.post("http://127.0.0.1:8000/connect", json=connection_obj)
    expected = {"status": "SUCCESS"}
    assert response.json() == expected


def test_get_all_connected():
    expected_len = 1
    response = requests.get("http://127.0.0.1:8000/connected")
    connection_len = len(response.json())
    assert connection_len == expected_len


def test_get_datasource_info():
    expected_tables = ["COPY_DB","EXCERCISE_DB","MANAGE_DB","MY_DB","SNOWFLAKE","SNOWFLAKE_SAMPLE_DATA"]
    response = requests.get("http://127.0.0.1:8000/data-source-info")
    ds_info_tables = list(response.json().keys())
    assert ds_info_tables == expected_tables


def test_select_connection():
    expected = "Selected snowflake"
    response = requests.post("http://127.0.0.1:8000/select", json={"connection": "snowflake"})
    assert response.json() == expected


def test_compilation():
    expected = "<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>name</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>Hello</td>\n    </tr>\n  </tbody>\n</table>"
    rule = {"engine":"trino","predicate":"Test","query_text":"Test(name: \"Hello\")"}
    response = requests.post("http://127.0.0.1:8000/compile", json=rule)
    assert response.json()["html"] == expected


def test_delete_all_connections():
    expected_len = 0
    requests.delete("http://127.0.0.1:8000/delete")
    response = requests.get("http://127.0.0.1:8000/connected")
    connection_len = len(response.json())
    assert connection_len == expected_len
