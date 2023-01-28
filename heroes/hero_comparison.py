from PIL import Image
import os
import cv2
import numpy as np


def similarity(image1, image2) -> float:
    return np.sum(cv2.subtract(image1, image2) ** 2) / (float(image1.shape[0] * image1.shape[1]))


class Hero:
    def __init__(self, image: Image, name: str):
        self.image, self.name = image, name

    def __repr__(self):
        return self.name


class Heroes:
    def __init__(self, hero_images_path: str):
        self.heroes: list[Hero] = list()
        for file in os.listdir(hero_images_path):
            # noinspection PyTypeChecker
            self.heroes.append(
                Hero(
                    name=file.replace(".png", ""),
                    image=cv2.cvtColor(
                        np.array(Image.open(f"{hero_images_path}/{file}")),
                        cv2.COLOR_BGR2GRAY
                    )
                )
            )

    def get_hero_name(self, hero_image: Image) -> Hero:
        hero_image = np.array(hero_image)
        hero_image = cv2.cvtColor(hero_image, cv2.COLOR_BGR2GRAY)
        results: list[tuple[float, Hero]] = list()
        for hero in self.heroes:
            results.append(
                (
                    similarity(hero_image, hero.image),
                    hero
                )
            )
        return sorted(results, key=lambda x: x[0])[0][1]


if __name__ == '__main__':
    d = Heroes("../assets/hero_images")
    result = d.get_hero_name(Image.open("Baptiste.png"))
