import sqlite3
import threading

import pytesseract
from PIL import Image

import heroes
import leaderboards
import database
import os
from rich.progress import track
from rich import print

from queue import Queue

dba = database.DatabaseAccess("./data/data.db")
target_season = "3_2"
dba.create_season(target_season)


queue = Queue()


def worker():
    while True:
        file = queue.get(block=True, timeout=1)
        print(f"{queue.qsize()} remaining", end='\r')
        role, region, _ = file.split("-")
        results = leaderboards.parse(
            region=region,
            role=role,
            image_path=f"./assets/leaderboard_images/{file}",
            assets_path="./assets/hero_images",
            temp_directory="./temp"
        )
        for i in results:
            dba.add_leaderboard_entry(seasonNumber=target_season, leaderboard_entry=i)
        queue.task_done()


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = \
        r"F:\Documents\Python Projects\top500-aggregator\bin\tesseract\tesseract.exe"

    lb_images = os.listdir("./assets/leaderboard_images")
    for item in lb_images:
        queue.put(item)
    for _ in range(7):
        threading.Thread(target=worker).start()
    queue.join()

