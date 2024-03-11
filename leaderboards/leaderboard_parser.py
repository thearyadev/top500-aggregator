from enum import Enum
from heroes import Heroes, hero_comparison
from PIL.Image import Image as ImageType
from typing import Final 
from pathlib import Path

ROW_HEIGHT_PX: Final[int] = 46
ROW_SKIP_PX: Final[int] = 13
COLUMN_WIDTH_PX: Final[int] = 100
COLUMN_SKIP_PX: Final[int] = 2



class ByNameEnum(Enum):
    @classmethod
    def by_name(cls, name):
        for enum_member, _ in cls.__members__.items():
            if enum_member == name:
                return cls[enum_member]
        return None


class Region(ByNameEnum):
    AMERICAS = 1
    EUROPE = 2
    ASIA = 3
    ALL = 4


class Role(ByNameEnum):
    TANK = 1
    DAMAGE = 2
    SUPPORT = 3
    ALL = 4


class LeaderboardEntry:
    def __init__(
        self,
        heroes: list[str],
        region: Region,
        role: Role,
    ):
        self.heroes = heroes
        self.region = region
        self.role = role

    def __repr__(self):
        return (
            f"LeaderboardEntry(heroes={self.heroes},"
            f" region={self.region}, role={self.role})"
        )

    def hasHero(self, hero: str) -> bool:
        if hero in self.heroes:
            return True
        return False

def crop_to_hero_section(pil_image: ImageType) -> ImageType:
    return pil_image.crop((1392, 294, 1696, 871))

def crop_split_row(pil_image: ImageType) -> list[ImageType]:
    current_offset_pos: int = 0
    o_width, o_height = pil_image.size
    result: list[ImageType] = list()
    for _ in range(10):
        result.append(
            pil_image.copy().crop(
                (
                    0,
                    current_offset_pos,
                    o_width,
                    min(current_offset_pos + ROW_HEIGHT_PX, o_height),
                )
            )
        )
        current_offset_pos += ROW_HEIGHT_PX + ROW_SKIP_PX
        if current_offset_pos >= o_height:
            break

    return result

def crop_split_column(pil_image: ImageType) -> list[ImageType]:
    current_offset_pos: int = 0
    result: list[ImageType] = list()
    o_width, o_height = pil_image.size
    for _ in range(3):
        result.append(
            pil_image.copy().crop(
                (
                    current_offset_pos,
                    0,
                    min(current_offset_pos + COLUMN_WIDTH_PX, o_width),
                    o_height
                )
            )
        )
        current_offset_pos += COLUMN_WIDTH_PX + COLUMN_SKIP_PX
        if current_offset_pos >= o_width:
            break
    return list(reversed(result)) # Hero placement has been reversed in Season 9 (blizzard moment.)

def parse_leaderboard_to_leaderboard_entries(leaderboard_image: ImageType, region: Region, role: Role, model_name) -> list[LeaderboardEntry]:
    hero_comp = Heroes()
    hero_section = crop_to_hero_section(leaderboard_image)
    row_entries = crop_split_row(hero_section)
    split_column_entries = [crop_split_column(row) for row in row_entries]
    results: list[LeaderboardEntry] = list() 
    for row in split_column_entries: # each record (10)

        results.append(LeaderboardEntry(
            heroes=[hero_comp.predict_hero_name_dhash_comparison(hero_image, Path(f"./models/{model_name}")) for hero_image in row], 
            role=role,
            region=region

        ))
    return results



