import pyautogui as pg
import time
from rich import print

def click_focus():
    pg.moveTo(122, 418)
    time.sleep(0.2)
    pg.click(122, 418)

def click_next_page():
    pg.moveTo(1010,908)
    time.sleep(0.1)
    pg.click(1010, 908)

def click_region_dropdown():
    pg.moveTo(1475, 256)
    time.sleep(1)
    pg.click(1475, 256)
    time.sleep(1)

def click_region_dropdown_americas():
        pg.moveTo(1476, 301)
        time.sleep(1.5)
        pg.mouseDown()
        pg.mouseUp()


def click_region_dropdown_europe():
        pg.moveTo(1476, 340)
        time.sleep(1.5)
        pg.mouseDown()
        pg.mouseUp()

def click_region_dropdown_asia():
        pg.moveTo(1476, 373)
        time.sleep(1.5)
        pg.mouseDown()
        pg.mouseUp()

def click_role_dropdown():
    pg.moveTo(1010, 261)
    time.sleep(1)
    pg.click(1010, 261)
    time.sleep(1)


def click_role_dropdown_tank():
        pg.moveTo(1007, 338)
        time.sleep(1.5)
        pg.mouseDown()
        pg.mouseUp()

def click_role_dropdown_damage():
        pg.moveTo(1007, 373)
        time.sleep(1.5)
        pg.mouseDown()
        pg.mouseUp()
    
def click_role_dropdown_support():
        pg.moveTo(1007, 412)
        time.sleep(1.5)
        pg.mouseDown()
        pg.mouseUp()


def collect_screens(role, region):
      for i in range(50):
            print(f"Role: {role} Region: {region} Page: {i + 1}           ", end="\r")
            click_focus()
            pg.screenshot().save(f"./assets/leaderboard_images/{role}-{region}-{i + 1}.png")
            time.sleep(1.5)
            click_next_page()

pg.PAUSE = 1

# click_next_page()



def main() -> int:
    click_focus()

    click_role_dropdown()
    click_role_dropdown_tank()

    click_region_dropdown()
    click_region_dropdown_americas()
    collect_screens(role="TANK", region="AMERICAS")

    click_region_dropdown()
    click_region_dropdown_europe()
    collect_screens(role="TANK", region="EUROPE")

    click_region_dropdown()
    click_region_dropdown_asia()
    collect_screens(role="TANK", region="ASIA")

    click_role_dropdown()
    click_role_dropdown_damage()
    click_region_dropdown()
    click_region_dropdown_americas()
    collect_screens(role="DAMAGE", region="AMERICAS")


    click_region_dropdown()
    click_region_dropdown_europe()
    collect_screens(role="DAMAGE", region="EUROPE")


    click_region_dropdown()
    click_region_dropdown_asia()
    collect_screens(role="DAMAGE", region="ASIA")


    click_role_dropdown()
    click_role_dropdown_support()

    click_region_dropdown()
    click_region_dropdown_americas()
    collect_screens(role="SUPPORT", region="AMERICAS")


    click_region_dropdown()
    click_region_dropdown_europe()
    collect_screens(role="SUPPORT", region="EUROPE")

    click_region_dropdown()
    click_region_dropdown_asia()
    collect_screens(role="SUPPORT", region="ASIA")

    return 0


if __name__ == "__main__":
      raise SystemExit(main())