import json
import os
from functools import lru_cache
from typing import Annotated, Any, Dict, List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
import heroes
import leaderboards
from statistic import (
    get_hero_occurrence_trend,
    get_hero_trends_all_heroes_by_region,
    get_mean,
    get_number_of_ohp,
    get_number_of_thp,
    get_occurrences,
    get_occurrences_most_played,
    get_stdev,
    get_variance,
)
from utils.raise_for_missing_env import raise_for_missing_env_vars

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
            "MISC": {
                "OHP": get_number_of_ohp(dataset),
                "THP": get_number_of_thp(dataset),
            },
        }

        # conducts calculations for mean variance and standard dev
        for key, val in data[s].items():
            if key != "MISC":
                graphData = data[s][key]["graph"]  # type: ignore
                data[s][key]["statistic"] = {  # type: ignore
                    "mean": round(get_mean(graphData), 3),
                    "variance": round(get_variance(graphData), 3),
                    "standard_deviation": round(get_stdev(graphData), 3),
                }
                data[s][key] = json.dumps(val)
    return data


@lru_cache
def trends_data() -> list[dict[str, list[int]]]:
    """
    Creates the data structure for use on the trends page.
    This function is cached.
    Returns:
        dict[str, dict[str, list[dict[str, int]]]]: data structure for use on the trends page
    """
    return get_hero_occurrence_trend(db=db)


@app.get("/{_}")
@app.get("/")
async def index_redirect(
    request: Request,
    seasons_list: Annotated[list[str], Depends(seasons_list)],
    seasons_data: Annotated[dict, Depends(season_data)],
):
    if "favicon.ico" in str(request.url):
        return FileResponse("static/favicon.ico")

    if "robots.txt" in str(request.url):
        return FileResponse("static/robots.txt")

    if "apple-touch-icon.png" in str(request.url):
        return FileResponse("static/apple-touch-icon.png")

    if "favicon-32x32.png" in str(request.url):
        return FileResponse("static/favicon-32x32.png")

    if "favicon-16x16.png" in str(request.url):
        return FileResponse("static/favicon-16x16.png")

    if "site.webmanifest" in str(request.url):
        return FileResponse("static/site.webmanifest")

    if "safari-pinned-tab.svg" in str(request.url):
        return FileResponse("static/safari-pinned-tab.svg")

    return await season(
        request,
        season_number=seasons_list[-1],
        seasons_data=seasons_data,
        seasons_list=seasons_list,
    )


@app.get("/season/{season_number}")
async def season(
    request: Request,
    season_number: str,
    seasons_data: Annotated[dict, Depends(season_data)],
    seasons_list: Annotated[list[str], Depends(seasons_list)],
):
    request.app.state.templates.env.filters["group_subseasons"] = group_subseasons

    if season_number in seasons_list:
        return templates.TemplateResponse(
            "season.html",
            {
                "request": request,
                "seasons": seasons_list,
                "currentSeason": season_number,
                "hero_colors": json.dumps(heroes.Heroes().hero_colors),
                **seasons_data[season_number],  # type: ignore
                **seasons_data[season_number]["MISC"],  # type: ignore
                # this does work. Im not sure why mypy is complaining.
                # It unpacks all of the chart datas into the global scope of the template
                "disclaimer": db.get_season_disclaimer(season_number),
            },
        )
    return RedirectResponse(f"/season{seasons_list[-1]}")


@app.get("/trends/seasonal")
async def trendsEndpoint(
    request: Request,
    seasons_list: Annotated[list[str], Depends(seasons_list)],
    trends_data: Annotated[dict, Depends(trends_data)],
):
    request.app.state.templates.env.filters["group_subseasons"] = group_subseasons

    return templates.TemplateResponse(
        "trends.html",
        {
            "request": request,
            "seasons": seasons_list,
            "trends": json.dumps(trends_data),
            "hero_colors": json.dumps(heroes.Heroes().hero_colors),
        },
    )


def group_subseasons(seasons: list[str]) -> dict[str, list[str]]:
    """
    Groups sub seasons together, to shrink the menu size.
    Args:
        seasons: list of seasons
    Returns:
        dict[str, list[str]]: dict of subseasons and their seasons
    """
    subseasons: dict[str, list[str]] = {}
    for season in seasons:
        subseason = season.split("_")[0]
        if subseason not in subseasons:
            subseasons[subseason] = []
        subseasons[subseason].append(season)
    return subseasons
