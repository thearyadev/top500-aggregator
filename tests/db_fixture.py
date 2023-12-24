import pytest
from database import DatabaseAccess
import os
from utils.raise_for_missing_env import raise_for_missing_env_vars
import dotenv


@pytest.fixture(scope="function")
def database():
    dotenv.load_dotenv()

    dba = DatabaseAccess(
        host=os.getenv("TESTING_MYSQLHOST") or raise_for_missing_env_vars(),
        user=os.getenv("TESTING_MYSQLUSER") or raise_for_missing_env_vars(),
        password=os.getenv("TESTING_MYSQLPASSWORD") or raise_for_missing_env_vars(),
        database=os.getenv("TESTING_MYSQLDATABASE") or raise_for_missing_env_vars(),
        port=os.getenv("TESTING_MYSQLPORT") or raise_for_missing_env_vars(),
    )
    dba.drop_and_rebuild_testing_db()
    yield dba
