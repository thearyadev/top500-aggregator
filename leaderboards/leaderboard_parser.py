import uuid

import numpy

from heroes import Hero, Heroes

try:
    import cv2
except Exception as e:
    pass
import numpy as np
from PIL import Image
import pytesseract
import string
import os
from enum import Enum


class Region(Enum):
    AMERICAS = 1
    EUROPE = 2
    ASIA = 3
    ALL = 4


class Role(Enum):
    TANK = 1
    DAMAGE = 2
    SUPPORT = 3
    ALL = 4


class LeaderboardEntry:
    def __init__(self, heroes: list[Hero] | str, games: int, region: Region = None, role: Role = None):
        self.heroes = heroes
        self.games = games
        self.region = region
        self.role = role

    def __repr__(self):
        return f"LeaderboardEntry(heroes={self.heroes}," \
               f" games_played={self.games}, region={self.region}, role={self.role})"

    def hasHero(self, hero: str) -> bool:
        if hero in self.heroes:
            return True
        return False


def clear_temp_dir(temp_dir: str) -> None:
    for f in os.listdir(temp_dir):
        os.remove(f"{temp_dir}/{f}")


def parse(image_path: str, assets_path: str, temp_directory: str, region: Region, role: Role) -> list[LeaderboardEntry]:
    results: list[LeaderboardEntry] = list()  # init return array
    heroComparor = Heroes(assets_path)  # class used to evaluate which hero is currently being looked at
    image_input: np.ndarray = cv2.imread(image_path)  # read the leaderboard image
    assert cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY).shape == (1080, 1920,)  # assert the shape as the calculations
    # below are predefined pixel values

    # defines the box around the first hero in a players top 3 on the lb
    starting_top_point: list[int] = [1306, 304]
    starting_bottom_point: list[int] = [1355, 354]
    # remember the vertical origin of the first hero
    x_origin: tuple[int, int] = (starting_top_point[0], starting_bottom_point[0],)
    for leaderboard_entry in range(10):  # 10 leaderboard entries per page
        heroes_played: list[Hero] = list()  # list of Hero. Saves the image in case its needed.
        for single_hero in range(3):  # a player can have 3 most played.
            if single_hero == 0:  # for the first iter
                # crop the image to the predefined box.
                modified: np.ndarray = image_input[starting_top_point[1]:starting_bottom_point[1],
                                       starting_top_point[0]:starting_bottom_point[0]]
                # write the file to the file system.
                # this is required because passing the cv2 numpy array directly
                # to the hero comparison caused failed tests
                # converting cv2 numpy array to PIL image did not work either.
                # save to filesystem, and let PIL reload it.
                cv2.imwrite(path := f"{temp_directory}/{uuid.uuid4().hex}.png", modified)
                heroes_played.append(
                    Hero(
                        name=heroComparor.get_hero_name(Image.open(path)).name,
                        image=modified
                    )  # creates and appends hero object to results
                )
                continue

            # moves box to the next hero in the leaderboard entry. This happens two times after the initial box.
            starting_top_point[0] += 52
            starting_bottom_point[0] += 52
            # write the file to the file system.
            # this is required because passing the cv2 numpy array directly
            # to the hero comparison caused failed tests
            # converting cv2 numpy array to PIL image did not work either.
            # save to filesystem, and let PIL reload it.
            modified: np.ndarray = image_input[starting_top_point[1]:starting_bottom_point[1],
                                   starting_top_point[0]:starting_bottom_point[0]]
            cv2.imwrite(path := f"{temp_directory}/{uuid.uuid4().hex}.png", modified)

            heroes_played.append(
                Hero(
                    name=heroComparor.get_hero_name(Image.open(path)).name,
                    image=modified
                )  # creates and appends hero object to results
            )

        # for the games played
        # move the box back and widen it to fit all the text.
        starting_top_point[0] -= 400
        starting_bottom_point[0] -= 250
        # crop the box
        # games_played_box: np.ndarray = image_input[starting_top_point[1]:starting_bottom_point[1],
        #                                starting_top_point[0]:starting_bottom_point[0]]
        # convert to rgb
        # gpb_rgb: np.ndarray = cv2.cvtColor(games_played_box, cv2.COLOR_BGR2RGB)
        # gpb_rgb = cv2.bitwise_not(gpb_rgb)
        # scan = None
        # for i in (13, 12, 11, 10,):
        #     try:
        #         scan = int(
        #             ''.join(
        #                 [c for c in pytesseract.image_to_string(gpb_rgb, config=f"--psm {i}") if c in string.digits]
        #             )
        #         )
        #
        #     except Exception as e:
        #         pass
        # if scan is None:
        #     raise Exception("the thing didnt work :(")
        # append results
        results.append(
            LeaderboardEntry(
                games=0,
                heroes=heroes_played,
                region=region,
                role=role
            )
        )
        # box start returns to the vertical origin (first hero top left corner)
        starting_top_point[0] = x_origin[0]
        starting_bottom_point[0] = x_origin[1]
        # translate the box down one row (next player in t500)
        starting_top_point[1] += 55
        starting_bottom_point[1] += 55
        # repeat 10 times

    # clear_temp_dir(temp_directory)

    return results


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = \
        r"F:\Documents\Python Projects\top500-aggregator\bin\tesseract\tesseract.exe"
    leaderboard: list[LeaderboardEntry] = parse(r"F:\Documents\Python Projects\top500-aggregator\assets\img.png",
                                                r"F:\Documents\Python Projects\top500-aggregator\assets\hero_images",
                                                r"../temp")
    for entry in leaderboard:
        print(entry)
