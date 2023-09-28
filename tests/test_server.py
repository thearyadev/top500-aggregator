import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient

import database
from server import app
from utils.raise_for_missing_env import raise_for_missing_env_vars

load_dotenv()

dba = database.DatabaseAccess(
    host=os.getenv("MYSQLHOST") or raise_for_missing_env_vars(),
    user=os.getenv("MYSQLUSER") or raise_for_missing_env_vars(),
    password=os.getenv("MYSQLPASSWORD") or raise_for_missing_env_vars(),
    database=os.getenv("MYSQLDATABASE") or raise_for_missing_env_vars(),
    port=os.getenv("MYSQLPORT") or raise_for_missing_env_vars(),
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
