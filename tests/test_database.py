import datetime
import random

import database
import heroes
from leaderboards import LeaderboardEntry, Region, Role

dba = database.DatabaseAccess(":memory:")

SEASON_ITERABLE = range(1, 6)
SUBSEASON_ITERABLE = range(1, 9)
ENTRIES_PER_TABLE = 4500
REGIONS = [Region.AMERICAS, Region.EUROPE, Region.ASIA]
ROLES = [Role.TANK, Role.DAMAGE, Role.SUPPORT]
HEROES = [
    heroes.Hero(image=None, image_array=None, name=h)
    for h in heroes.Heroes("./assets/hero_images").hero_labels.keys()
]


def test_info_table_create():
    assert dba.create_info_table() == None

    START_DATE = datetime.datetime(2020, 1, 1)
    for season in SEASON_ITERABLE:
        for subseason in SUBSEASON_ITERABLE:
            assert (
                dba.add_info_entry(
                    f"season_{season}_{subseason}",
                    (START_DATE + datetime.timedelta(days=(7 * season))).timestamp(),
                    "disclaimer",
                )
                == None
            )


def test_info_table_get():
    seasons: list[str] = dba.get_seasons()
    assert len(seasons) == (SEASON_ITERABLE.stop - 1) * (SUBSEASON_ITERABLE.stop - 1)
    for season in seasons:
        assert isinstance(season, str)
        assert len(season.split("_")) == 2


def test_season_table_create():
    for season in SEASON_ITERABLE:
        for subseason in SUBSEASON_ITERABLE:
            assert dba.create_season(f"{season}_{subseason}") == None


def test_season_table_add_entries():
    for season in SEASON_ITERABLE:
        for subseason in SUBSEASON_ITERABLE:
            for _ in range(0, ENTRIES_PER_TABLE):
                assert (
                    dba.add_leaderboard_entry(
                        f"{season}_{subseason}",
                        LeaderboardEntry(
                            region=random.choice(REGIONS).name,
                            role=random.choice(ROLES).name,
                            games=0,
                            heroes=[
                                random.choice(HEROES),
                                random.choice(HEROES),
                                random.choice(HEROES),
                            ],
                        ),
                    )
                    == None
                )


def test_get_all_records():
    for season in SEASON_ITERABLE:
        for subseason in SUBSEASON_ITERABLE:
            assert (
                len(dba.get_all_records(f"{season}_{subseason}")) == ENTRIES_PER_TABLE
            )
