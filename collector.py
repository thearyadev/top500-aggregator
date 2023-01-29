import pyautogui
import pyautogui as pg
import leaderboards
import time
import os
import uuid

pg.PAUSE = 2
SETTINGS = {
    "role": leaderboards.Role.TANK.name,
    "region": leaderboards.Region.ASIA.name
}


def next_page():
    pyautogui.click(1004, 884)


def generate_name() -> str:
    return f"{SETTINGS.get('role')}-{SETTINGS.get('region')}-{uuid.uuid4().hex[:8]}.png"


def main():
    for i in range(50):  # 50 pages
        pg.screenshot(f"./assets/leaderboard_images/{generate_name()}", region=(0, 0, 1920, 1080,))
        next_page()


if __name__ == '__main__':
    n = f"./assets/leaderboard_images/{generate_name()}"

    pg.screenshot(n, region=(0, 0, 1920, 1080,))
    print(n)