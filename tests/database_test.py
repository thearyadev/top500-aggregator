from .db_fixture import database
from database import DatabaseAccess
import pytest
from leaderboards import LeaderboardEntry, Region, Role
from heroes import Hero
import random


@pytest.mark.parametrize(
    "test",
    [
        ("season_2_8",),
        ("iojasldk",),
        ("0a89sduoljasdsakdjhasdhjaksjdhaiushdo129sahojdhasdad"),
    ],
)
def test_add_info_entry(test: str, database: DatabaseAccess):
    database.add_info_entry("season_2_8", disclaimer="disclaimer", patch_notes=None)


@pytest.mark.parametrize("test", [f"{i}_8" for i in range(0, 100, 10)])
def test_create_season(test: str, database: DatabaseAccess):
    database.create_season(test)


@pytest.mark.parametrize(
    "test",
    [
        LeaderboardEntry(
            heroes=["Kiriko", "Widowmaker", "Hanzo"],
            games=0,
            region=random.sample([Region.ASIA, Region.AMERICAS, Region.EUROPE], k=1)[0],
            role=random.sample([Role.DAMAGE, Role.TANK, Role.SUPPORT], k=1)[0],
        )
        for _ in range(10)
    ],
)
def test_add_leaderboard_entry(test: LeaderboardEntry, database: DatabaseAccess):
    season_num = "1_8"
    database.create_season(season_num)
    database.add_leaderboard_entry(season_num, test)


def test_get_all_records(database: DatabaseAccess):
    season_num = "1_8"
    database.create_season(season_num)
    _ = [
        database.add_leaderboard_entry(
            season_num,
            LeaderboardEntry(
                heroes=["Kiriko", "Widowmaker", "Hanzo"],
                games=0,
                region=random.sample(
                    [Region.ASIA, Region.AMERICAS, Region.EUROPE], k=1
                )[0],
                role=random.sample([Role.DAMAGE, Role.TANK, Role.SUPPORT], k=1)[0],
            ),
        )
        for _ in range(10)
    ]

    query = database.get_all_records(season_num)

    assert len(query) == 10
    assert isinstance(query[0], LeaderboardEntry)
    assert isinstance(query[0].role, Role)
    assert isinstance(query[0].region, Region)
    for hero in query[0].heroes:
        assert isinstance(hero, str)


@pytest.mark.parametrize(
    "test,expected",
    [
        (None, []),
        (["season_1_8", "season_2_8"], ["1_8", "2_8"]),
        pytest.param(
            "oasidjald", [], marks=pytest.mark.xfail(reason="Invalid season name")
        ),
    ],
)
def test_get_seasons(
    test: str | list[str] | None, expected: list[str], database: DatabaseAccess
):
    if test is None:
        assert database.get_seasons() == expected

    if isinstance(test, list):
        for season in test:
            database.add_info_entry(season, None, None)
        assert database.get_seasons() == expected

    if isinstance(test, str):
        database.add_info_entry(test, None, None)
        database.get_seasons()
