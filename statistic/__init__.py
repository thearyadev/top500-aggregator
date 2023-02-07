import statistics

import database
import leaderboards
from heroes import allHeroes


def convert_dict_to_hero_count_array(data: dict) -> list[dict]:
    return [{"hero": i[0], "count": i[1]} for i in data.items()]


def extract_games_played(i: leaderboards.LeaderboardEntry):
    return i.games


def filter_games_results(i: leaderboards.LeaderboardEntry) -> bool:
    return 25 <= i.games <= 725


def get_occurrences(
        *,
        data: list[leaderboards.LeaderboardEntry],
        region: leaderboards.Region = None
) -> list[dict]:
    results: dict[str, int] = {}
    acceptedRegions: list[leaderboards.Region] = [region, ]
    if region == leaderboards.Region.ALL:
        acceptedRegions = [
            leaderboards.Region.AMERICAS,
            leaderboards.Region.ASIA,
            leaderboards.Region.EUROPE,
        ]

    for entry in data:
        if entry.region not in acceptedRegions: continue
        for hero in entry.heroes:
            if hero in results:
                results[hero] += 1
                continue
            results[hero] = 1
    try:
        results.pop("Blank")
    except KeyError:
        pass
    return sorted(convert_dict_to_hero_count_array(results), key=lambda x: x["count"], reverse=True)


def get_occurrences_most_played(
        *,
        data: list[leaderboards.LeaderboardEntry],
        role: leaderboards.Role,
        region: leaderboards.Region,
        mostPlayedSlot: int
) -> list[dict]:
    mostPlayedSlot = mostPlayedSlot - 1
    results: dict[str, int] = {}
    acceptedRegions: list[leaderboards.Region] = [region, ]
    acceptedRoles: list[leaderboards.Role] = [role, ]

    if region == leaderboards.Region.ALL:
        acceptedRegions = [
            leaderboards.Region.AMERICAS,
            leaderboards.Region.ASIA,
            leaderboards.Region.EUROPE,
        ]

    if role == leaderboards.Role.ALL:
        acceptedRoles = [
            leaderboards.Role.SUPPORT,
            leaderboards.Role.DAMAGE,
            leaderboards.Role.TANK
        ]

    for entry in data:
        if entry.region not in acceptedRegions: continue
        if entry.role not in acceptedRoles: continue

        mostPlayedHero: str = entry.heroes[mostPlayedSlot]
        if mostPlayedHero in results:
            results[mostPlayedHero] += 1
            continue
        results[mostPlayedHero] = 1
    try:
        results.pop("Blank")
    except KeyError:
        pass
    return sorted(convert_dict_to_hero_count_array(results), key=lambda x: x["count"], reverse=True)


def get_avg_games_played_by_region(
        *,
        data: list[leaderboards.LeaderboardEntry],
        region: leaderboards.Region
) -> list[dict]:
    results: dict[str, float] = {}

    for entry in filter(filter_games_results, data):
        if entry.region != region: continue
        if entry.role.name in results:
            results[entry.role.name] += entry.games / 500
            continue
        results[entry.role.name] = entry.games / 500

    return sorted(convert_dict_to_hero_count_array(results), key=lambda x: x["count"], reverse=True)


def convert_count_dict_to_array(data: list[dict]) -> list[int | float]:
    return [entry['count'] for entry in data]


def get_mean(data: list[dict]) -> float:
    return statistics.fmean(convert_count_dict_to_array(data))


def get_variance(data: list[dict]) -> float:
    return statistics.variance(convert_count_dict_to_array(data))


def get_stdev(data: list[dict]) -> float:
    return statistics.stdev(convert_count_dict_to_array(data))


def get_games_played_max(data: list[leaderboards.LeaderboardEntry]) -> int:
    return max(map(extract_games_played, filter(filter_games_results, data)))


def get_games_played_min(data: list[leaderboards.LeaderboardEntry]) -> int:
    return min(map(extract_games_played, filter(filter_games_results, data)))


def get_games_played_total(data: list[leaderboards.LeaderboardEntry]) -> int:
    return sum(map(extract_games_played, filter(filter_games_results, data)))


def get_number_of_ohp(data: list[leaderboards.LeaderboardEntry]) -> int:
    return len([i for i in data if i.heroes[1] == "Blank"])


def get_number_of_thp(data: list[leaderboards.LeaderboardEntry]) -> int:
    return len([i for i in data if i.heroes[2] == "Blank"])


def get_hero_trends(db: database.DatabaseAccess) -> dict[str, list[list[str, int, int, int]]]:
    results: dict[str, list[list[str, int, int, int]]] = dict()

    # hero, list[point(seasonNumber, americas, europe, asia)]
    for hero in allHeroes:
        results[hero] = list()
        for season in db.get_seasons():
            results[hero].append(
                [
                    season,
                    db.get_total_hero_occurrence_count(hero, region=leaderboards.Region.AMERICAS, seasonNumber=season),
                    db.get_total_hero_occurrence_count(hero, region=leaderboards.Region.EUROPE, seasonNumber=season),
                    db.get_total_hero_occurrence_count(hero, region=leaderboards.Region.ASIA, seasonNumber=season),
                ]
            )
    return results
