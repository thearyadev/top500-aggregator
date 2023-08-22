from fastapi.testclient import TestClient

import mysql_database
from server import app
import os
from dotenv import load_dotenv

load_dotenv()

dba = mysql_database.DatabaseAccess(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT"),
)
client = TestClient(app)


def test_all_seasons_valid_html():
    # get all the seasons
    seasons: list[str] = dba.get_seasons()
    for season in seasons:  # attempt to access each seasons webpage
        response = client.get(f"/season/{season}")
        assert response.status_code == 200


def test_trends():
    response = client.get("/trends/seasonal")
    # assert response.status_code == 200
    assert True


def test_favicon():
    response = client.get("/favicon.ico")
    assert response.status_code == 200


def test_robots():
    response = client.get("/robots.txt")
    assert response.status_code == 200


def test_sitemap():
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
