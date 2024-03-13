import sys
sys.path.append(".")
import json
from leaderboards import parse_leaderboard_to_leaderboard_entries, Role, Region
from rich import print
from rich.prompt import Prompt
from pathlib import Path
from PIL import Image
from PIL.Image import Image as ImageType
from dataclasses import dataclass

@dataclass
class ImageOutline:
    role: str
    region: str
    image: ImageType




def load_images(dir: Path) -> list[ImageOutline]:
    return [ImageOutline(role=f.name.split("-")[0], region=f.name.split("-")[1], image=Image.open(f)) for f in dir.iterdir()]




def main() -> int:
    image_dir = Path(Prompt.ask("Image Directory", default="assets/leaderboard_images"))
    season_id = Prompt.ask("Season Identifier")
    disclaimer = Prompt.ask("Disclaimer")
    images = load_images(image_dir)

    entries: list[dict[str, str]] = list()
    for i, image in enumerate(images):
        print(f"{i} of {len(images)} ({(i/len(images)) * 100})")
        role, region = Role.by_name(image.role), Region.by_name(image.region)
        if role is None or region is None:
            raise Exception("A file is not named correctly.")
        result = parse_leaderboard_to_leaderboard_entries(
            image.image,
            role=role,
            region=region
        )
        for r in result:
            entries.append({
                "role": str(role),
                "region": str(region),
                "firstMostPlayed": r.heroes[0],
                "secondMostPlayed": r.heroes[1],
                "thirdMostPlayed": r.heroes[2],
            })

    data = {
        "metadata": {
            "id": season_id,
            "disclaimer": disclaimer
        },
        "entries": entries
    }
    with open(f"./data/{season_id}.json") as json_file:
        json.dump(data, json_file)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
