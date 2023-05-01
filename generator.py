import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image
from rich.console import Console
from rich.progress import Progress, track
from rich.prompt import Prompt

import database
import leaderboards

console = Console()
dba = database.DatabaseAccess("./data/data.db")


def worker(file: str):
    role, region, _ = file.split("-")  # parse the filename
    results = leaderboards.parse(  # parse the leaderboard
        image_path=os.path.join("./assets/leaderboard_images", file),
        assets_path="./assets/hero_images",
        role=role,
        region=region,
        model_path=model_path,
    )
    for i in results:
        # Populate the database with the parsed results
        dba.add_leaderboard_entry(seasonNumber=target_season, leaderboard_entry=i)
        pass


def main():
    global target_season, model_path  # globals so the worker threads can access them
    # sorry

    target_season = "4_69"
    model_path = r"models\thearyadev-2023-04-30\thearyadev-2023-04-30.model"
    dba.create_season(seasonNumber=target_season)

    files = os.listdir("./assets/leaderboard_images")
    max_workers = 16
    progress = Progress()
    with progress:
        progress_bar = progress.add_task(
            "[red]Parsing Leaderboard Images...", total=len(files)
        )
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(worker, file) for file in files]
            for future in as_completed(futures):
                progress.advance(progress_bar)


if __name__ == "__main__":
    main()
