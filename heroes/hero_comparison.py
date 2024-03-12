from PIL.Image import Image
from PIL import Image as ImageOpen
from functools import lru_cache
from pathlib import Path
from typing import Any

import imagehash

model_cache: dict[Any, Any] = dict()


def predict_hero_name_dhash_comparison(image: Image) -> str:
    input_hash = imagehash.dhash(image)
    hashes = []
    heroes = []
    for f in Path("./assets/heroes").iterdir():
        hashes.append(get_image_hash(f))
        heroes.append(f.name.replace(".png", "").replace("2", ""))

    diffs: list[int] = [abs(input_hash - h) for h in hashes]
    ret = sorted(zip(diffs, heroes), key=lambda x: x[0])
    return ret[0][1]


@lru_cache
def get_image_hash(path: Path) -> imagehash.ImageHash:
    return imagehash.dhash(ImageOpen.open(path))
