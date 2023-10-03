from __future__ import annotations

import importlib  # importlib is used to import the model from the model file

import numpy as np

# conditionally imported; type not required
model_cache: dict[str, NNModel] = {}  # type: ignore


class Hero:
    """
    Hero class to store hero data. This class has some reduenancy but is utilized for better organization in some areas of this project
    """

    # conditionally imported; type not required
    def __init__(self, image: Image.Image | None, name: str):  # type: ignore
        self.image, self.name = image, name

    def __repr__(self):
        return self.name


class Heroes:
    def __init__(self):
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
            38: "LifeWeaver",
            39: "Illari",
        }
        self.hero_role: dict[str, str] = {
            "Ana": "SUPPORT",
            "Ashe": "DAMAGE",
            "Baptiste": "SUPPORT",
            "Bastion": "DAMAGE",
            "Blank": "NA",
            "Blank": "NA",
            "Brigitte": "SUPPORT",
            "Cassidy": "DAMAGE",
            "D.Va": "TANK",
            "Doomfist": "TANK",
            "Echo": "DAMAGE",
            "Genji": "DAMAGE",
            "Hanzo": "DAMAGE",
            "Illari": "SUPPORT",
            "Junker Queen": "TANK",
            "Junkrat": "DAMAGE",
            "Kiriko": "SUPPORT",
            "Lucio": "SUPPORT",
            "Mei": "DAMAGE",
            "Mercy": "SUPPORT",
            "Moira": "SUPPORT",
            "Orisa": "TANK",
            "Pharah": "DAMAGE",
            "Ramattra": "TANK",
            "Reaper": "DAMAGE",
            "Reinhardt": "TANK",
            "Roadhog": "TANK",
            "Sigma": "TANK",
            "Sojourn": "DAMAGE",
            "Soldier 76": "DAMAGE",
            "Sombra": "DAMAGE",
            "Symmetra": "DAMAGE",
            "Torbjorn": "DAMAGE",
            "Tracer": "DAMAGE",
            "Widowmaker": "DAMAGE",
            "Winston": "TANK",
            "Wrecking Ball": "TANK",
            "Zarya": "TANK",
            "Zenyatta": "SUPPORT",
            "LifeWeaver": "SUPPORT",
        }

    def predict_hero_name(self, image_data: np.ndarray, model_name: str) -> Hero:
        """Predicts the hero name from an image using a neural network model.

        Args:
            model_name: name of model in models dir
            image_data (np.ndarray): array of image data
            model_path (str): path to the Fashion MNIST model

        Returns:
            Hero: Hero object with the predicted hero name; this is the hero with the highest confidence level. This object only contains the hero name.
        """
        # Read an image
        # image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Resize to the same size as Fashion MNIST images

        from PIL import Image
        import cv2  # type: ignore
        from neural_network import Model as NNModel

        image_data = cv2.resize(image_data, (49, 50))

        # Reshape and scale pixel data
        image_data = (image_data.reshape(1, -1).astype(np.float32) - 127.5) / 127.5

        # Load the model

        if model_name not in model_cache:
            model = (
                importlib.import_module(f"models.{model_name}")
                .Model()
                .load(f"models/{model_name}/{model_name}.model")
            )

            model_cache[model_name] = model
        else:
            model = model_cache[model_name]

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
                results.append((1, Hero(image=None, name=hero_name)))
            else:
                results.append((0, Hero(image=None, name=hero_name)))
            i += 1

        results = sorted(results, key=lambda x: x[0], reverse=True)

        return results[0][1]
