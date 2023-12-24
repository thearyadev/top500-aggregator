from statistic import *
import pytest
from leaderboards import LeaderboardEntry, Region, Role


def test_convert_dict_to_hero_count_array():
    test = {"Ana": 912, "Moira": 71, "Widowmaker": 300}

    result = convert_dict_to_hero_count_array(test)
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, dict)
        assert item["hero"] in test.keys()
        assert item["count"] == test[item["hero"]]


@pytest.mark.parametrize(
    "data, role, region, mostPlayedSlot, expected",
    [
        (
            [
                LeaderboardEntry(
                    heroes=["Kiriko", "Ana", "Lucio"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Brigitte", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
            ],
            leaderboards.Role.SUPPORT,
            leaderboards.Region.AMERICAS,
            1,
            [{"hero": "Ana", "count": 2}, {"hero": "Kiriko", "count": 1}],
        ),
        (
            [
                LeaderboardEntry(
                    heroes=["Kiriko", "Ana", "Lucio"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Brigitte", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Sojourn", "Widowmaker", "Tracer"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.DAMAGE,
                ),
            ],
            leaderboards.Role.DAMAGE,
            leaderboards.Region.AMERICAS,
            1,
            [{"hero": "Sojourn", "count": 1}],
        ),
        (
            [
                LeaderboardEntry(
                    heroes=["Kiriko", "Ana", "Lucio"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Brigitte", "Zenyatta"],
                    games=0,
                    region=Region.EUROPE,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
            ],
            leaderboards.Role.SUPPORT,
            leaderboards.Region.EUROPE,
            1,
            [{"hero": "Ana", "count": 1}],
        ),
        (
            [
                LeaderboardEntry(
                    heroes=["Kiriko", "Ana", "Lucio"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Brigitte", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
            ],
            leaderboards.Role.SUPPORT,
            leaderboards.Region.AMERICAS,
            2,
            [
                {"hero": "Ana", "count": 1},
                {"hero": "Brigitte", "count": 1},
                {"hero": "Moira", "count": 1},
            ],
        ),
    ],
)
def test_get_occurrences_most_played(data, role, region, mostPlayedSlot, expected):
    assert (
        get_occurrences_most_played(
            data=data, role=role, region=region, mostPlayedSlot=mostPlayedSlot
        )
        == expected
    )


@pytest.mark.parametrize(
    "test,expected",
    [
        ([{"hero": "Ana", "count": 2}, {"hero": "Moira", "count": 5}], [2, 5]),
        (
            [{"hero": "Ana", "count": 2}],
            [
                2,
            ],
        ),
    ],
)
def test_convert_count_dict_to_array(test, expected):
    result = convert_count_dict_to_array(test)
    assert isinstance(result, list)
    assert isinstance(result[0], int)
    assert result == expected


@pytest.mark.parametrize(
    "season_data,hero,expected",
    [
        (
            [
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Moira", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Illari"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
            ],
            "Ana",
            4,
        ),
        (
            [
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Moira", "Lucio", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Illari"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
            ],
            "Moira",
            5,
        ),
        (
            [
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Moira", "Lucio", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Illari"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
            ],
            "Illari",
            1,
        ),
        (
            [
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Moira", "Lucio", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Zenyatta"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
                LeaderboardEntry(
                    heroes=["Ana", "Moira", "Illari"],
                    games=0,
                    region=Region.AMERICAS,
                    role=Role.SUPPORT,
                ),
            ],
            "Widowmaker",
            0,
        ),
    ],
)
def test_get_hero_occurrences_single_season(season_data, hero, expected):
    result = get_hero_occurrences_single_season(season_data, hero)
    assert result == expected
