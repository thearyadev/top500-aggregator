import os
import time

from PIL import Image

from neural_network import Model

try:
    import cv2
except Exception:
    # In the Railway server, cv2 is not installed. This try except will catch the import error when using this module in Railway
    pass
import math
import uuid

import numpy as np


def similarity(image1, image2) -> float:
    # Substract method
    return np.sum(cv2.subtract(image1, image2) ** 2) / (
        float(image1.shape[0] * image1.shape[1])
    )


def dist(hist1, hist2) -> float:
    # Historogram comparison
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)


def psnr(image1, image2) -> float:
    # Peak Signal to Noise Ratio comparison
    mse = np.mean((image1 - image2) ** 2)
    result = -1
    if mse == 0:
        result = 100
    PIXEL_MAX = 255.0
    result = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return result


class Hero:
    """
    Hero class to store hero data. This class has some reduenancy but is utilized for better organization in some areas of this project
    """

    def __init__(self, image: Image, image_array: list, name: str):
        self.image, self.image_array, self.name = image, image_array, name

    def __repr__(self):
        return self.name


class Heroes:
    def __init__(self, hero_images_path: str):
        self.heroes: list[Hero] = list()
        # update this with new heroes and their label as used during training.
        self.hero_labels: dict[int, str] = {
            0: "Ana",
            1: "Ashe",
            2: "Baptiste",
            3: "Bastion",
            4: "Blank",
            5: "Blank",
            6: "Brigitte",
            7: "Cassidy",
            8: "D.Va",
            9: "Doomfist",
            10: "Echo",
            11: "Genji",
            12: "Hanzo",
            13: "Junker Queen",
            14: "Junkrat",
            15: "Kiriko",
            16: "Lucio",
            17: "Mei",
            18: "Mercy",
            19: "Moira",
            20: "Orisa",
            21: "Pharah",
            22: "Ramattra",
            23: "Reaper",
            24: "Reinhardt",
            25: "Roadhog",
            26: "Sigma",
            27: "Sojourn",
            28: "Soldier 76",
            29: "Sombra",
            30: "Symmetra",
            31: "Torbjorn",
            32: "Tracer",
            33: "Widowmaker",
            34: "Winston",
            35: "Wrecking Ball",
            36: "Zarya",
            37: "Zenyatta",
        }

        # load hero images from file system. This is used for the calculate_hero_name method, which is now deprecated.
        # this may be removed in a future version.
        for file in os.listdir(hero_images_path):
            # noinspection PyTypeChecker
            self.heroes.append(
                Hero(
                    name=file.replace(".png", ""),
                    image=cv2.cvtColor(
                        np.array(Image.open(f"{hero_images_path}/{file}")),
                        cv2.COLOR_BGR2GRAY,  # loads images as grayscale
                    ),
                    image_array=np.array(Image.open(f"{hero_images_path}/{file}")),
                )
            )

    def predict_hero_name(self, image_data: np.ndarray, model_path: str) -> Hero:
        """Predicts the hero name from an image using a neural network model.

        Args:
            image_data (np.ndarray): array of image data
            model_path (str): path to the Fashion MNIST model

        Returns:
            Hero: Hero object with the predicted hero name; this is the hero with the highest confidence level. This object only contains the hero name.
        """
        # Read an image
        # image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Resize to the same size as Fashion MNIST images
        image_data = cv2.resize(image_data, (49, 50))

        # Reshape and scale pixel data
        image_data = (image_data.reshape(1, -1).astype(np.float32) - 127.5) / 127.5

        # Load the model
        model = Model().load(model_path)

        # Predict on the image
        confidences = model.predict(image_data)

        # Get prediction instead of confidence levels
        predictions = model.output_layer_activation.predictions(confidences)

        results: list[tuple[float, Hero]] = list()
        i = 0

        for (
            label,
            hero_name,
        ) in self.hero_labels.items():  # match prediction to the hero
            if label == predictions[0]:
                results.append((1, Hero(image=None, image_array=None, name=hero_name)))
            else:
                results.append((0, hero_name))
            i += 1

        results = sorted(results, key=lambda x: x[0], reverse=True)

        return results[0][1]

    def calculate_hero_name(self, image_data: np.ndarray) -> Hero:
        """Uses a combination of different methods to calculate the hero name from an image. This currently does not work very well...

        Now deprecated. Use predict_hero_name instead.
        Args:
            image_data (np.ndarray): array of image data

        Returns:
            Hero: hero object with hero name only.
        """
        hero_array = np.array(image_data)  # color
        hero_image = cv2.cvtColor(hero_array, cv2.COLOR_BGR2GRAY)  # grayscale
        hero_hist = cv2.calcHist([hero_image], [0], None, [256], [0, 256])
        cv2.normalize(hero_hist, hero_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

        results_subs: list[tuple[float, Hero]] = list()
        results_dist: list[tuple[float, Hero]] = list()
        results_psnr: list[tuple[float, Hero]] = list()

        for hero in self.heroes:
            query_hist = cv2.calcHist([hero.image], [0], None, [256], [0, 256])
            cv2.normalize(
                query_hist, query_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX
            )

            results_subs.append((similarity(hero_image, hero.image), hero))

            results_dist.append((dist(hero_hist, query_hist), hero))

            results_psnr.append((psnr(hero_array, hero.image_array), hero))
        results_subs = sorted(results_subs, key=lambda x: x[0])
        results_dist = sorted(results_dist, key=lambda x: x[0])
        results_psnr = sorted(results_subs, key=lambda x: x[0], reverse=True)
        # print(f"Confidence: {result[0][0]}")
        # time.sleep(0.1)
        # If two or more values match they are returned, if there are not a definitive match, substract value is returned
        if (
            results_subs[0][1] == results_dist[0][1]
            or results_subs[0][1] == results_psnr[0][1]
        ):
            return results_subs[0][1]
        elif results_subs[0][1] == results_psnr[0][1]:
            return results_subs[0][1]
        else:
            return results_subs[0][1]


if __name__ == "__main__":
    # im1 = cv2.cvtColor(cv2.imread("../leaderboards/blank2.png"), cv2.COLOR_BGR2GRAY)
    # im2 = cv2.cvtColor(cv2.imread("../assets/hero_images/Blank.png"), cv2.COLOR_BGR2GRAY)
    # im3 = cv2.cvtColor(cv2.imread("../assets/hero_images/Echo.png"), cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("echo_gray", im3)
    # cv2.imwrite("blank_gray", im1)
    #
    #
    # print(similarity(im1, im2))
    # print(similarity(im1, im3))
    # print(similarity(im2, im3))
    d = Heroes("assets\hero_images").get_hero_name(
        Image.open("G:/temp\Blank2/4cb57b5224974d3dbab9ec7e95377349.png")
    )
    print(d)
