import json
import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
import leaderboards
from statistic import (
    get_hero_occurrence_trend,
    get_mean,
    get_occurrences,
    get_occurrences_most_played,
    get_stdev,
    get_variance,
    get_hero_occurrences_single_season,
)
from utils.raise_for_missing_env import raise_for_missing_env_vars
import heroes
import numpy as np

load_dotenv()
templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.state.templates = templates  # type: ignore
app.mount("/static", StaticFiles(directory="static"), name="static")

db = database.DatabaseAccess(
    host=os.getenv("MYSQLHOST") or raise_for_missing_env_vars(),
    user=os.getenv("MYSQLUSER") or raise_for_missing_env_vars(),
    password=os.getenv("MYSQLPASSWORD") or raise_for_missing_env_vars(),
    database=os.getenv("MYSQLDATABASE") or raise_for_missing_env_vars(),
    port=os.getenv("MYSQLPORT") or raise_for_missing_env_vars(),
)


@lru_cache
def seasons_list() -> list[str]:
    """
    Wrapper for db.get_seasons() to cache the result
    Returns:
        list[str]: list of seasons
    """
    return db.get_seasons()


def map_to_label_count_array(data: dict):
    result: dict[str, Any] = dict()
    for season in data.keys():
        result[season] = dict()
        for chart, values in data[season].items():
            result[season][chart] = {
                "graph": {"labels": list(), "values": list()},
                "statistic": values["statistic"],
            }
            for hero in values["graph"]:
                result[season][chart]["graph"]["labels"].append(hero["hero"])
                result[season][chart]["graph"]["values"].append(hero["count"])
    return result


@lru_cache
def season_data() -> dict[str, Any]:
    """
    Creates the data structure for use on the season page.
    This function is cached.
    Returns:
        dict[str, Any]: data structure for use on the season page
        see function implementation for exact data structure shape. (sorry)

    """
    data: dict = dict()
    for s in seasons_list():
        dataset: list[leaderboards.LeaderboardEntry] = db.get_all_records(s)
        data[s] = {
            # occurrences first most played
            "OFMP_SUPPORT_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_SUPPORT_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_SUPPORT_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_DAMAGE_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_DAMAGE_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_DAMAGE_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_TANK_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_TANK_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_TANK_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_SUPPORT_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_DAMAGE_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=1,
                ),
            },
            "OFMP_TANK_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=1,
                ),
            },
            # occurrences second most played
            "OSMP_SUPPORT_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_SUPPORT_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_SUPPORT_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_DAMAGE_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_DAMAGE_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_DAMAGE_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_TANK_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_TANK_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_TANK_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_SUPPORT_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_DAMAGE_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=2,
                ),
            },
            "OSMP_TANK_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=2,
                ),
            },
            # occurrences third most played
            "OTMP_SUPPORT_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_SUPPORT_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_SUPPORT_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_DAMAGE_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_DAMAGE_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_DAMAGE_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_TANK_AMERICAS": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.AMERICAS,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_TANK_EUROPE": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.EUROPE,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_TANK_ASIA": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.ASIA,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_SUPPORT_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.SUPPORT,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_DAMAGE_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.DAMAGE,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=3,
                ),
            },
            "OTMP_TANK_ALL": {
                "graph": get_occurrences_most_played(
                    data=dataset,
                    role=leaderboards.Role.TANK,
                    region=leaderboards.Region.ALL,
                    mostPlayedSlot=3,
                ),
            },
            "O_ALL_AMERICAS": {
                "graph": get_occurrences(
                    data=dataset,
                    region=leaderboards.Region.AMERICAS,
                ),
            },
            "O_ALL_EUROPE": {
                "graph": get_occurrences(
                    data=dataset,
                    region=leaderboards.Region.EUROPE,
                ),
            },
            "O_ALL_ASIA": {
                "graph": get_occurrences(data=dataset, region=leaderboards.Region.ASIA),
            },
            "O_ALL_ALL": {
                "graph": get_occurrences(data=dataset, region=leaderboards.Region.ALL),
            },
        }

        # conducts calculations for mean variance and standard dev
        for key, val in data[s].items():
            graphData = data[s][key]["graph"]  # type: ignore
            data[s][key]["statistic"] = {  # type: ignore
                "mean": round(get_mean(graphData), 3),
                "variance": round(get_variance(graphData), 3),
                "standard_deviation": round(get_stdev(graphData), 3),
            }
    return map_to_label_count_array(data)


@lru_cache
def trends_data() -> list[dict[str, list[int]]]:
    """
    Creates the data structure for use on the trends page.
    This function is cached.
    Returns:
        dict[str, dict[str, list[dict[str, int]]]]: data structure for use on the trends page
    """
    return get_hero_occurrence_trend(db=db)


@lru_cache
def std_dev_data() -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = dict()
    for season in seasons_list():
        support, tank, damage = (
            [
                get_hero_occurrences_single_season(
                    db.get_all_records(seasonNumber=season), name
                )
                for name, role in heroes.Heroes().hero_role.items()
                if role == "SUPPORT"
            ],
            [
                get_hero_occurrences_single_season(
                    db.get_all_records(seasonNumber=season), name
                )
                for name, role in heroes.Heroes().hero_role.items()
                if role == "TANK"
            ],
            [
                get_hero_occurrences_single_season(
                    db.get_all_records(seasonNumber=season), name
                )
                for name, role in heroes.Heroes().hero_role.items()
                if role == "DAMAGE"
            ],
        )

        # feeling creative.
        # this file is a writeoff anyway.
        def filter_fn(percentile):
            def filter_fn_inner(x):
                return x > percentile
            return filter_fn_inner
        exclude_percentile = 10
        support = list(filter(filter_fn(np.percentile(support, exclude_percentile)), support))
        damage = list(filter(filter_fn(np.percentile(damage, exclude_percentile)), damage))
        tank = list(filter(filter_fn(np.percentile(tank, exclude_percentile)), tank))

        result[season] = dict(SUPPORT=np.std(support), DAMAGE=np.std(damage), TANK=np.std(tank))
    return result


@app.get("/d/seasons")
async def seasons_list_d():
    return Response(json.dumps(seasons_list()), media_type="application/json")


@app.get("/d/single_season_std_by_role/{season}")
async def single_season_std_by_role(season: str):
    return Response(
        content=json.dumps(std_dev_data()[season]), media_type="application/json"
    )


@app.get("/chart/{season}")
async def chart_data(season: str):
    return Response(
        content=json.dumps(season_data()[season]), media_type="application/json"
    )


@app.get("/chart/trend/d")
async def trend_chart_data():
    return Response(content=json.dumps(trends_data()), media_type="application/json")
