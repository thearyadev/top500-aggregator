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
    ROLES = [r.name for r in list(leaderboards.Role) if r not in (leaderboards.Role.ALL, )]
    REGIONS = [r.name for r in list(leaderboards.Region) if r != leaderboards.Region.ALL]

    for role in ROLES:
        for region in REGIONS:
            if role in ("TANK", "DAMAGE"):
                if region in ("AMERICAS", "EUROPE", "ASIA"):
                    continue
            SETTINGS["role"] = role
            SETTINGS["region"] = region
            print(f"SET TO: {SETTINGS}")
            time.sleep(10)

            for i in range(50):  # 50 pages
                print(f"screenshotting page: {i+1}")
                pg.screenshot(f"./assets/leaderboard_images/{generate_name()}", region=(0, 0, 1920, 1080,))
                next_page()


if __name__ == '__main__':
    main()
    # pg.screenshot("./assets/leaderboard_images/SUPPORT-ASIA-MANUAL120983.png", region=(0, 0, 1920, 1080,))
