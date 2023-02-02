import pyautogui
import pyautogui as pg
import leaderboards
import time
import os
import uuid

pg.PAUSE = 2
SETTINGS = {
    "role": None,
    "region": None
}


def next_page():
    pyautogui.click(1004, 884)


def generate_name() -> str:
    return f"{SETTINGS.get('role')}-{SETTINGS.get('region')}-{uuid.uuid4().hex[:8]}.png"


def main():
    ROLES = [r.name for r in list(leaderboards.Role) if r not in (leaderboards.Role.ALL, leaderboards.Role.TANK)]
    REGIONS = [r.name for r in list(leaderboards.Region) if r != leaderboards.Region.ALL]

    for role in ROLES:
        for region in REGIONS:
            SETTINGS["role"] = role
            SETTINGS["region"] = region
            if role == leaderboards.Role.DAMAGE.name  and region == leaderboards.Region.AMERICAS.name: continue
            print(f"SET TO: {SETTINGS}")
            time.sleep(10)
            for i in range(50):  # 50 pages
                print(f"screenshotting page: {i+1}")
                pg.screenshot(f"./assets/leaderboard_images/{generate_name()}", region=(0, 0, 1920, 1080,))
                next_page()


if __name__ == '__main__':
    main()
