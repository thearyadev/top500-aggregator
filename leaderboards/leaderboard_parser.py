from __future__ import annotations

from enum import Enum
from heroes import predict_hero_name_dhash_comparison
from PIL.Image import Image as ImageType
from typing import Final, TypeVar

ROW_HEIGHT_PX: Final[int] = 46
ROW_SKIP_PX: Final[int] = 13
COLUMN_WIDTH_PX: Final[int] = 100
COLUMN_SKIP_PX: Final[int] = 2

T = TypeVar('T', bound="ByNameEnum")
class ByNameEnum(Enum):
    @classmethod
    def by_name(cls: type[T], name: str) -> T | None:
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
    ) -> None:
        self.heroes = heroes
        self.region = region
        self.role = role

    def __repr__(self) -> str:
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
                    o_height,
                )
            )
        )
        current_offset_pos += COLUMN_WIDTH_PX + COLUMN_SKIP_PX
        if current_offset_pos >= o_width:
            break
    return result

def parse_leaderboard_to_leaderboard_entries(
    leaderboard_image: ImageType, region: Region, role: Role
) -> list[LeaderboardEntry]:
    hero_section = crop_to_hero_section(leaderboard_image)
    row_entries = crop_split_row(hero_section)
    split_column_entries = [crop_split_column(row) for row in row_entries]
    results: list[LeaderboardEntry] = list()
    for row in split_column_entries:  # each record (10)
        computed_result = LeaderboardEntry(
                heroes=[
                    predict_hero_name_dhash_comparison(hero_image) for hero_image in row
                ],
                role=role,
                region=region,
            )
        blank_filtered_result = [hero for hero in computed_result.heroes if hero != "Blank"]
        while len(blank_filtered_result) != 3:
            blank_filtered_result.append("Blank")
        computed_result.heroes = blank_filtered_result

        results.append(computed_result)
    return results
