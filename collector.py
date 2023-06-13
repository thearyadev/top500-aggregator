import os
import time
import uuid

import pyautogui
import pyautogui as pg

import leaderboards

pg.PAUSE = 2  # delay for each pg actin
SETTINGS = {
    "role": None,
    "region": None,
    "page": 1,
}  # settings for the leaderboard page

SUBFOLDER = "34"

def next_page():
    pyautogui.click(1004, 884)  # click next page button


def generate_name() -> str:  # gens a name
    return f"{SETTINGS.get('role')}-{SETTINGS.get('region')}-{SETTINGS.get('page')}.png"


def main():
    ROLES = [
        r.name for r in list(leaderboards.Role) if r not in (leaderboards.Role.ALL, )
    ]
    REGIONS = [
        r.name for r in list(leaderboards.Region) if r != leaderboards.Region.ALL
    ]
    for role in ROLES:
        for region in REGIONS:  # loop through all roles and regions
            SETTINGS["role"] = role
            SETTINGS["region"] = region  # update settings
            print(f"SET TO: {SETTINGS}")  # prompt
            pages = int(input("How many pages? "))
            time.sleep(5)  # wait for user to get to the page

            for i in range(pages):  # 50 pages
                SETTINGS["page"] = i + 1  # set page
                print(f"screenshotting page: {i+1}")  # prompt
                pg.screenshot(
                    f"./assets/leaderboard_images/{generate_name()}",
                    region=(  # full screenshot
                        0,
                        0,
                        1920,
                        1080,
                    ),
                )
                next_page()  # go next page


if __name__ == "__main__":
    main()
    # pg.screenshot(f"./assets/leaderboard_images/MANUAL/SUPPORT-ASIA-44.png",region=(0,0,1920,1080,),)