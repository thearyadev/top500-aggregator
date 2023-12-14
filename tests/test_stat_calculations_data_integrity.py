"""This tests the integrity of ./archive/latest.sql by running all calculations on it.
The goal of these tests is to catch errors that would cause invalid data or prevent the server from starting
"""

import os

from dotenv import load_dotenv

import database
from leaderboards import Region, Role
from statistic import (
    get_hero_trends_all_heroes_by_region,
    get_mean,
    get_number_of_ohp,
    get_number_of_thp,
    get_occurrences,
    get_occurrences_most_played,
    get_stdev,
    get_variance,
    get_hero_occurrence_trend
)
from utils.raise_for_missing_env import raise_for_missing_env_vars

load_dotenv()
dba = database.DatabaseAccess(
    host=os.getenv("MYSQLHOST") or raise_for_missing_env_vars(),
    user=os.getenv("MYSQLUSER") or raise_for_missing_env_vars(),
    password=os.getenv("MYSQLPASSWORD") or raise_for_missing_env_vars(),
    database=os.getenv("MYSQLDATABASE") or raise_for_missing_env_vars(),
    port=os.getenv("MYSQLPORT") or raise_for_missing_env_vars(),
)

data = []

for season in dba.get_seasons():
    data.append(dba.get_all_records(seasonNumber=season))


def test_get_occurrences():
    for season_data in data:
        for region in [Region.AMERICAS, Region.EUROPE, Region.ASIA]:
            assert get_occurrences(data=season_data, region=region)


def test_get_occurrences_most_played():
    for season_data in data:
        for region in [Region.AMERICAS, Region.EUROPE, Region.ASIA]:
            for role in [Role.DAMAGE, Role.SUPPORT, Role.TANK]:
                for most_played_slot in (1, 2, 3):
                    assert get_occurrences_most_played(
                        data=season_data,
                        region=region,
                        role=role,
                        mostPlayedSlot=most_played_slot,
                    )


def test_get_mean():
    for season_data in data:
        for region in [Region.AMERICAS, Region.EUROPE, Region.ASIA]:
            for role in [Role.DAMAGE, Role.SUPPORT, Role.TANK]:
                for most_played_slot in (1, 2, 3):
                    assert get_mean(
                        data=get_occurrences_most_played(
                            data=season_data,
                            region=region,
                            role=role,
                            mostPlayedSlot=most_played_slot,
                        )
                    )

                assert get_mean(data=get_occurrences(data=season_data, region=region))


def test_get_variance():
    for season_data in data:
        for region in [Region.AMERICAS, Region.EUROPE, Region.ASIA]:
            for role in [Role.DAMAGE, Role.SUPPORT, Role.TANK]:
                for most_played_slot in (1, 2, 3):
                    assert get_variance(
                        data=get_occurrences_most_played(
                            data=season_data,
                            region=region,
                            role=role,
                            mostPlayedSlot=most_played_slot,
                        )
                    )

                assert get_variance(
                    data=get_occurrences(data=season_data, region=region)
                )


def test_get_stdev():
    for season_data in data:
        for region in [Region.AMERICAS, Region.EUROPE, Region.ASIA]:
            for role in [Role.DAMAGE, Role.SUPPORT, Role.TANK]:
                for most_played_slot in (1, 2, 3):
                    assert get_stdev(
                        data=get_occurrences_most_played(
                            data=season_data,
                            region=region,
                            role=role,
                            mostPlayedSlot=most_played_slot,
                        )
                    )

                assert get_stdev(data=get_occurrences(data=season_data, region=region))


def test_get_hero_trends():
    assert print(get_hero_trends_all_heroes_by_region(dba)) or True


def test_get_hero_occurrence_trends():
    num_seasons = len(dba.get_seasons())
    trends_data = get_hero_occurrence_trend(dba)
    for hero in trends_data:
        assert hero['name']
        assert hero['data']
        assert len(hero['data']) == num_seasons


def test_get_number_of_ohp():
    for season_data in data:
        assert get_number_of_ohp(season_data)


def test_get_number_of_thp():
    for season_data in data:
        assert get_number_of_thp(season_data)
