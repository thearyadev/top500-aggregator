import os
import time
import uuid

import pyautogui
import pyautogui as pg

import leaderboards

pg.PAUSE = 2
SETTINGS = {"role": None, "region": None}


def next_page():
    pyautogui.click(1004, 884)


def generate_name() -> str:
    return f"{SETTINGS.get('role')}-{SETTINGS.get('region')}-{uuid.uuid4().hex[:8]}.png"


def main():
    ROLES = [
        r.name for r in list(leaderboards.Role) if r not in (leaderboards.Role.ALL,)
    ]
    REGIONS = [
        r.name for r in list(leaderboards.Region) if r != leaderboards.Region.ALL
    ]

    for role in ROLES:
        for region in REGIONS:
            if role in ("TANK"):
                if region in ("AMERICAS", "EUROPE"):
                    continue
            SETTINGS["role"] = role
            SETTINGS["region"] = region
            print(f"SET TO: {SETTINGS}")
            time.sleep(10)

            for i in range(50):  # 50 pages
                print(f"screenshotting page: {i+1}")
                pg.screenshot(
                    f"./assets/leaderboard_images/{generate_name()}",
                    region=(
                        0,
                        0,
                        1920,
                        1080,
                    ),
                )
                next_page()


if __name__ == "__main__":
    # main()
   # path = r"assets\test_leaderboard_images\DAMAGE_S4_P50_AMERCIAS"
   # path = r"assets\test_leaderboard_images\DAMAGE_S4_P49_AMERCIAS"
    #path = r"assets\test_leaderboard_images\DAMAGE_S4_P47_AMERCIAS"
    path = r"assets\test_leaderboard_images\TANK_S4_P49_AMERCIAS"
    os.mkdir(path)
    pg.screenshot(
        path + r"\LB-IMG.png",
        region=(
            0,
            0,
            1920,
            1080,
        ),
    )
    f = open(path + r"\key.json", "w+")
    f.close()
