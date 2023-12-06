import sys
sys.path.append(".")
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import database
from PIL import Image
from rich.console import Console
from rich.progress import Progress, track
from rich.prompt import Prompt
from utils.raise_for_missing_env import raise_for_missing_env_vars

import leaderboards
import dotenv

dotenv.load_dotenv()

console = Console()
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

    results = leaderboards.parse(  # parse the leaderboard
        image_path=os.path.join("./assets/leaderboard_images", file),
        assets_path="./assets/hero_images",
        role=role,
        region=region,
        model_name=model_name,
    )

    for i in results:
        if i.heroes[0].name != "Blank":
            dba.add_leaderboard_entry(seasonNumber=target_season, leaderboard_entry=i)

def main():
    global target_season, model_name  # globals so the worker threads can access them
    # sorry

    target_season = "6_8"
    model_name = "thearyadev-2023-08-25"
    dba.create_season(seasonNumber=target_season)

    files = os.listdir("./assets/leaderboard_images")
    max_workers = 1
    progress = Progress()

    with progress:
        progress_bar = progress.add_task(
            "[red]Parsing Leaderboard Images...", total=len(files)
        )
        for file in files:
            worker(file)

        # with ThreadPoolExecutor(max_workers=max_workers) as executor:
        #     futures = [executor.submit(worker, file) for file in files]
        #     for future in as_completed(futures):
        #         progress.advance(progress_bar)


if __name__ == "__main__":
    main()
