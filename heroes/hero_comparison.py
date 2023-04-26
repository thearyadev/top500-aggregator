import time

from neural_network import Model

from PIL import Image
import os

try:
    import cv2
except Exception:
    # In the Railway server, cv2 is not installed. This try except will catch the import error when using this module in Railway
    pass
import numpy as np
import uuid
import math


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
    def __init__(self, image: Image, image_array: list, name: str):
        self.image, self.image_array, self.name = image, image_array, name

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
                        cv2.COLOR_BGR2GRAY,
                    ),
                    image_array=np.array(Image.open(f"{hero_images_path}/{file}")),
                )
            )

    def predict_hero_name(self, image_path: str) -> Hero:
        # Read an image
        image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Resize to the same size as Fashion MNIST images
        image_data = cv2.resize(image_data, (49, 50))

        # Reshape and scale pixel data
        image_data = (image_data.reshape(1, -1).astype(np.float32) - 127.5) / 127.5

        # Load the model
        model = Model().load("neural_network/top_500_mnist.model")

        # Predict on the image
        confidences = model.predict(image_data)

        # Get prediction instead of confidence levels
        predictions = model.output_layer_activation.predictions(confidences)

        results: list[tuple[float, Hero]] = list()
        i = 0

        for hero in self.heroes:
            if i == predictions[0]:
                results.append((1, hero))
            else:
                results.append((0, hero))
            i += 1

        results = sorted(results, key=lambda x: x[0], reverse=True)

        return results[0][1]

    def get_hero_name(self, hero_image: Image) -> Hero:
        hero_array = np.array(hero_image)
        hero_image = cv2.cvtColor(hero_array, cv2.COLOR_BGR2GRAY)
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
