import uuid

from heroes import Hero, Heroes
import cv2
import numpy as np
from PIL import Image


class LeaderboardEntry:
    def __init__(self, heroes: list[Hero], rank: int):
        self.heroes = heroes
        self.rank = rank


def parse(image_path: str, assets_path: str, temp_directory: str) -> list[LeaderboardEntry]:
    results: list[LeaderboardEntry] = list()
    heroComparor = Heroes(assets_path)
    image_input: np.ndarray = cv2.imread(image_path)
    assert cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY).shape == (1079, 1919,)

    starting_top_point: list[int] = [1306, 300]
    starting_bottom_point: list[int] = [1355, 350]
    x_origin: tuple[int, int] = (starting_top_point[0], starting_bottom_point[0],)
    for leaderboard_entry in range(10):
        heroes_played: list[Hero] = list()
        for single_hero in range(3):
            if single_hero == 0:
                modified: np.ndarray = image_input[starting_top_point[1]:starting_bottom_point[1], starting_top_point[0]:starting_bottom_point[0]]
                cv2.imwrite(path := f"{temp_directory}/{uuid.uuid4().hex}.png", modified)
                heroes_played.append(
                    Hero(
                        name=heroComparor.get_hero_name(Image.open(path)).name,
                        image=modified
                    )
                )
                continue
            starting_top_point[0] += 52
            starting_bottom_point[0] += 52

            modified: np.ndarray = image_input[starting_top_point[1]:starting_bottom_point[1],
                                               starting_top_point[0]:starting_bottom_point[0]]
            cv2.imwrite(path := f"{temp_directory}/{uuid.uuid4().hex}.png", modified)

            heroes_played.append(
                Hero(
                    name=heroComparor.get_hero_name(Image.open(path)).name,
                    image=modified
                )
            )
        results.append(
            LeaderboardEntry(
                rank=0,
                heroes=heroes_played
            )
        )
        starting_top_point[0] = x_origin[0]
        starting_bottom_point[0] = x_origin[1]
        starting_top_point[1] += 55
        starting_bottom_point[1] += 55
    return results


if __name__ == "__main__":
    leaderboard: list[LeaderboardEntry] = parse(r"F:\Documents\Python Projects\top500-aggregator\src\img_3.png",
                                                r"F:\Documents\Python Projects\top500-aggregator\assets\hero_images",
                                                r"../temp")
    for entry in leaderboard:
        print(entry.heroes)