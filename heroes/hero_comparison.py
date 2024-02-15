from __future__ import annotations
from PIL.Image import Image
import torch
import importlib
from pathlib import Path


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
            40: "Mauga",
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
            "Mauga": "TANK",
        }

        self.hero_colors: dict[str, str] = {
            "Ana": "#8796B6",
            "Ashe": "#808284",
            "Baptiste": "#7DB8CE",
            "Bastion": "#8c998c",
            "Blank": "#000000",
            "Brigitte": "#957D7E",
            "Cassidy": "#b77e80",
            "D.Va": "#F59CC8",
            "Doomfist": "#947F80",
            "Echo": "#A4CFF9",
            "Genji": "#9FF67D",
            "Hanzo": "#BDB894",
            "Illari": "#B3A58A",
            "Junker Queen": "#89B2D5",
            "Junkrat": "#F0BE7C",
            "Kiriko": "#D4868F",
            "Lucio": "#91CD7D",
            "Mei": "#81AFED",
            "Mercy": "#F4EFBF",
            "Moira": "#9d86e5",
            "Orisa": "#76967B",
            "Pharah": "#768BC8",
            "Ramattra": "#9B89CE",
            "Reaper": "#8D797E",
            "Reinhardt": "#9EA8AB",
            "Roadhog": "#BC977E",
            "Sigma": "#9CA7AA",
            "Sojourn": "#D88180",
            "Soldier 76": "#838A9C",
            "Sombra": "#887EBC",
            "Symmetra": "#98C1D1",
            "Torbjorn": "#C38786",
            "Tracer": "#DE9D7D",
            "Widowmaker": "#A583AB",
            "Winston": "#A7AABE",
            "Wrecking Ball": "#E09C7C",
            "Zarya": "#F291BB",
            "Zenyatta": "#F5EC91",
            "LifeWeaver": "#E0B6C5",
            "Mauga": "#DC847D",
        }

    def predict_hero_name(self, image: Image, model_directory: Path) -> str:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        NNModel = importlib.import_module(f"models.{model_directory.name}.model").NNModel
        transformer = importlib.import_module(f"models.{model_directory.name}.model").transformer

        st_dict = torch.load(model_directory / "model.pth")
        model = NNModel(num_classes=40)
        model.to(device)
        model.load_state_dict(st_dict)
        model.eval()

        model.to(device)
        with open(model_directory / "classes", "r") as f:
            classes = f.readlines()

        with torch.no_grad():
            tensor_img = transformer(image).unsqueeze(0).to(device)
            output = model(tensor_img)
            prediction = int(classes[int(torch.argmax(output, dim=1).item())])
        
        return self.hero_labels[prediction]
