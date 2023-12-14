import statistics

import database
import leaderboards
from heroes import Hero, Heroes


def convert_dict_to_hero_count_array(data: dict) -> list[dict]:
    return [{"hero": i[0], "count": i[1]} for i in data.items()]


def extract_games_played(i: leaderboards.LeaderboardEntry):
    return i.games


def filter_games_results(i: leaderboards.LeaderboardEntry) -> bool:
    return 25 <= i.games <= 725


def get_occurrences(
    *,
    data: list[leaderboards.LeaderboardEntry],
    region: leaderboards.Region | None = None,
    role: leaderboards.Role | None = None,
) -> list[dict]:
    results: dict[str, int] = {}
    acceptedRegions: list[leaderboards.Region] = [
        region or leaderboards.Region.ALL,
    ]
    if region == leaderboards.Region.ALL:
        acceptedRegions = [
            leaderboards.Region.AMERICAS,
            leaderboards.Region.ASIA,
            leaderboards.Region.EUROPE,
        ]

    for entry in data:
        if role and entry.role != role:
            continue

        if entry.region not in acceptedRegions:
            continue
        for hero in entry.heroes:
            if isinstance(
                hero, str
            ):  # stupid me! I designed the leaderboard entry to be able to accept list[hero] and list[str]
                if hero in results:
                    results[hero] += 1
                    continue
                results[hero] = 1
    try:
        results.pop("Blank")
        results.pop("Blank2")
    except KeyError:
        pass
    return sorted(
        convert_dict_to_hero_count_array(results),
        key=lambda x: x["count"],
        reverse=True,
    )


def get_occurrences_most_played(
    *,
    data: list[leaderboards.LeaderboardEntry],
    role: leaderboards.Role,
    region: leaderboards.Region,
    mostPlayedSlot: int,
) -> list[dict]:
    mostPlayedSlot = mostPlayedSlot - 1
    results: dict[str, int] = {}
    acceptedRegions: list[leaderboards.Region] = [
        region,
    ]
    acceptedRoles: list[leaderboards.Role] = [
        role,
    ]

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
            leaderboards.Role.TANK,
        ]

    for entry in data:
        if entry.region not in acceptedRegions:
            continue
        if entry.role not in acceptedRoles:
            continue

        mostPlayedHero: Hero | str = entry.heroes[mostPlayedSlot]
        if isinstance(mostPlayedHero, str):
            if mostPlayedHero in results:
                results[mostPlayedHero] += 1
                continue
            results[mostPlayedHero] = 1

    try:
        results.pop("Blank")
        results.pop("Blank2")
    except KeyError:
        pass
    return sorted(
        convert_dict_to_hero_count_array(results),
        key=lambda x: x["count"],
        reverse=True,
    )


def get_avg_games_played_by_region(
    *, data: list[leaderboards.LeaderboardEntry], region: leaderboards.Region
) -> list[dict]:
    results: dict[str, float] = {}

    for entry in filter(filter_games_results, data):
        if entry.region != region:
            continue
        if entry.role.name in results:
            results[entry.role.name] += entry.games / 500
            continue
        results[entry.role.name] = entry.games / 500

    return sorted(
        convert_dict_to_hero_count_array(results),
        key=lambda x: x["count"],
        reverse=True,
    )


def convert_count_dict_to_array(data: list[dict]) -> list[int | float]:
    return [entry["count"] for entry in data]


def get_mean(data: list[dict]) -> float:
    return statistics.fmean(convert_count_dict_to_array(data))


def get_variance(data: list[dict]) -> float:
    return statistics.variance(convert_count_dict_to_array(data))


def get_stdev(data: list[dict]) -> float:
    return statistics.stdev(convert_count_dict_to_array(data))


def get_games_played_max(data: list[leaderboards.LeaderboardEntry]) -> int:
    # return max(map(extract_games_played, filter(filter_games_results, data)))
    return 0


def get_games_played_min(data: list[leaderboards.LeaderboardEntry]) -> int:
    # return min(map(extract_games_played, filter(filter_games_results, data)))
    return 0


def get_games_played_total(data: list[leaderboards.LeaderboardEntry]) -> int:
    # return sum(map(extract_games_played, filter(filter_games_results, data)))
    return 0


def get_number_of_ohp(data: list[leaderboards.LeaderboardEntry]) -> int:
    return len([i for i in data if i.heroes[1] == "Blank" or i.heroes[1] == "Blank2"])


def get_number_of_thp(data: list[leaderboards.LeaderboardEntry]) -> int:
    return len([i for i in data if i.heroes[1] == "Blank" or i.heroes[1] == "Blank2"])


def fill_missing_heroes(hero_dict: dict[str, int]) -> dict[str, int]:
    for hero in Heroes().hero_labels.values():
        if hero in ("Blank", "Blank2"):
            continue

        if hero not in hero_dict:
            hero_dict[hero] = 0
    return hero_dict


def fill_missing_hero_by_role(
    hero_dict: dict[str, int], roleFilter: str
) -> dict[str, int]:
    heroes_present: list[str] = list(hero_dict.keys())
    for hero, role in Heroes().hero_role.items():
        if hero in ("Blank", "Blank2"):
            continue

        if role == roleFilter:
            if hero not in heroes_present:
                hero_dict[hero] = 0
    return hero_dict


def get_hero_trends_all_heroes_by_region(
    db: database.DatabaseAccess,
) -> dict[str, dict[str, list[dict[str, int]]]]:
    # NOTE: This function does multiple cross type mutations to the results variable.
    #      I've ignored type checks for the mutations. The result type is accurate.
    #      I tried to strictly type this but it made the code redundant/verbose and
    #      I don't think it's worth it.
    results: dict[str, dict[str, list[dict[str, int]]]] = {}

    # iter seasons
    for season in db.get_seasons():
        # init season
        results[season] = {"SUPPORT": dict(), "DAMAGE": dict(), "TANK": dict()}  # type: ignore
        # get season data
        seasonData = db.get_all_records(season)
        # iter season data
        for entry in seasonData:  # entry is a leaderboard entry
            for hero in entry.heroes:  # skip blanks
                if hero in ("Blank", "Blank2"):
                    continue

                # increment or init hero in dict. for its role
                if hero not in results[season][entry.role.name]:
                    results[season][entry.role.name][hero] = 0  # type: ignore
                results[season][entry.role.name][hero] += 1  # type: ignore
    # filtering
    for season, roleDict in results.items():
        # iter data
        for role, heroesInRole in roleDict.items():
            # fill all missing heroes for respective roles
            results[season][role] = fill_missing_hero_by_role(heroesInRole, role)  # type: ignore
            # convert {hero: count} to [{hero: hero, count: count}]
            results[season][role] = convert_dict_to_hero_count_array(
                results[season][role]  # type: ignore
            )
            # sort by hero name
            results[season][role] = sorted(
                results[season][role], key=lambda x: x["hero"], reverse=False
            )
    return results


def get_hero_occurrences_single_season(
    season_data: list[leaderboards.LeaderboardEntry], hero: str
) -> int:
    count: int = 0
    for entry in season_data:
        if hero in entry.heroes:
            count += 1
    return count


def get_hero_occurrence_trend(
    db: database.DatabaseAccess,
) -> list[dict[str, list[int]]]:
    result: list[dict[str, list[int]]] = list()
    leaderboard_data: dict[str, list[leaderboards.LeaderboardEntry]] = {
        s: db.get_all_records(s) for s in db.get_seasons()
    }
    for hero in [h for h in Heroes().hero_labels.values() if h != "Blank"]:
        hero_result = {"name": hero, "data": list()}

        for season in db.get_seasons():
            hero_result["data"].append(  # type: ignore
                get_hero_occurrences_single_season(leaderboard_data[season], hero=hero)
            )

        result.append(hero_result)  # type: ignore
    return result
