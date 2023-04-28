import os
import sqlite3
import threading
from queue import Queue

import pytesseract
from PIL import Image
from rich import print
from rich.progress import track

import database
import heroes
import leaderboards

dba = database.DatabaseAccess("./data/data.db")
target_season = "4_2"
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
            temp_directory="G:/temp"
        )
        for i in results:
            dba.add_leaderboard_entry(seasonNumber=target_season, leaderboard_entry=i)
        queue.task_done()


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = \
        r"G:\autop\Desktop\Estudio\Proyectos\Overwatch Picker\Top500\top500-aggregator\bin\tesseract\tesseract.exe"

    lb_images = os.listdir("./assets/leaderboard_images")
    for item in lb_images:
        queue.put(item)
    for _ in range(7):
        threading.Thread(target=worker).start()
    #threading.Thread(target=worker).start()
    queue.join()

