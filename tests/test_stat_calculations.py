from legacy_database import DatabaseAccess
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
)

import os


from dotenv import load_dotenv
import mysql_database

load_dotenv()

dba = mysql_database.DatabaseAccess(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT"),
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
    assert get_hero_trends_all_heroes_by_region(dba)


def test_get_number_of_ohp():
    for season_data in data:
        assert get_number_of_ohp(season_data)


def test_get_number_of_thp():
    for season_data in data:
        assert get_number_of_thp(season_data)
