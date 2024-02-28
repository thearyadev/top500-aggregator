import sys

sys.path.append(".")
import os

import dotenv

import database
import leaderboards
from utils.raise_for_missing_env import raise_for_missing_env_vars
from PIL import Image

dotenv.load_dotenv()

dba = database.DatabaseAccess(
    host=os.getenv("MYSQLHOST") or raise_for_missing_env_vars(),
    user=os.getenv("MYSQLUSER") or raise_for_missing_env_vars(),
    password=os.getenv("MYSQLPASSWORD") or raise_for_missing_env_vars(),
    database=os.getenv("MYSQLDATABASE") or raise_for_missing_env_vars(),
    port=os.getenv("MYSQLPORT") or raise_for_missing_env_vars(),
)


def worker(file: str):
    role, region, _ = file.split("-")  # parse the filename
    role = leaderboards.Role.by_name(role)
    region = leaderboards.Region.by_name(region)

    results = leaderboards.parse_leaderboard_to_leaderboard_entries(
            leaderboard_image=Image.open(f"./assets/leaderboard_images/{file}"),
            region=region, # type: ignore
            role=role, # type: ignore
            model_name="thearyadev-initial-15-02-2024",
        )


    for i in results:
        if i.heroes[0] != "Blank":
            dba.add_leaderboard_entry(seasonNumber=target_season, leaderboard_entry=i)


def main():
    global target_season, model_name  # globals so the worker threads can access them
    # sorry

    target_season = "9"
    dba.create_season(seasonNumber=target_season)

    files = os.listdir("./assets/leaderboard_images")

    for file in files:
        worker(file)


if __name__ == "__main__":
    dba.add_info_entry("season_9", "This season is a test of the new top 500 hero classifier model. There may be issues with this page. This dataset was recorded on Febuary 29, 2AM EDT.", None )
    # main()
