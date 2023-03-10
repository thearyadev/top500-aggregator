from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json

import leaderboards
from statistic import (get_occurrences_most_played, get_occurrences, get_avg_games_played_by_region, get_mean,
                       get_stdev, get_variance, get_number_of_ohp, get_number_of_thp, get_games_played_max,
                       get_games_played_min, get_games_played_total, get_hero_trends)
import database

templates = Jinja2Templates(directory="templates")
db = database.DatabaseAccess("./data/data.db")

seasons = db.get_seasons()
data = dict()
trends: dict[str, list[list[str, int, int, int]]] = get_hero_trends(db)
hits = 0


def calculate():
    for s in seasons:
        dataset: list[leaderboards.LeaderboardEntry] = db.get_all_records(s)
        data[s] = {
            # occurrences first most played
            "OFMP_SUPPORT_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                           role=leaderboards.Role.SUPPORT,
                                                                           region=leaderboards.Region.AMERICAS,
                                                                           mostPlayedSlot=1)
                                      },
            "OFMP_SUPPORT_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                         role=leaderboards.Role.SUPPORT,
                                                                         region=leaderboards.Region.EUROPE,
                                                                         mostPlayedSlot=1)
                                    },
            "OFMP_SUPPORT_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                       role=leaderboards.Role.SUPPORT,
                                                                       region=leaderboards.Region.ASIA,
                                                                       mostPlayedSlot=1)
                                  },
            "OFMP_DAMAGE_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                          role=leaderboards.Role.DAMAGE,
                                                                          region=leaderboards.Region.AMERICAS,
                                                                          mostPlayedSlot=1)
                                     },
            "OFMP_DAMAGE_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                        role=leaderboards.Role.DAMAGE,
                                                                        region=leaderboards.Region.EUROPE,
                                                                        mostPlayedSlot=1)
                                   },
            "OFMP_DAMAGE_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.DAMAGE,
                                                                      region=leaderboards.Region.ASIA,
                                                                      mostPlayedSlot=1)
                                 },
            "OFMP_TANK_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                        role=leaderboards.Role.TANK,
                                                                        region=leaderboards.Region.AMERICAS,
                                                                        mostPlayedSlot=1)
                                   },
            "OFMP_TANK_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.TANK,
                                                                      region=leaderboards.Region.EUROPE,
                                                                      mostPlayedSlot=1)
                                 },
            "OFMP_TANK_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                    role=leaderboards.Role.TANK,
                                                                    region=leaderboards.Region.ASIA,
                                                                    mostPlayedSlot=1)
                               },
            "OFMP_SUPPORT_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.SUPPORT,
                                                                      region=leaderboards.Region.ALL,
                                                                      mostPlayedSlot=1)
                                 },
            "OFMP_DAMAGE_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                     role=leaderboards.Role.DAMAGE,
                                                                     region=leaderboards.Region.ALL,
                                                                     mostPlayedSlot=1)
                                },
            "OFMP_TANK_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                   role=leaderboards.Role.TANK,
                                                                   region=leaderboards.Region.ALL,
                                                                   mostPlayedSlot=1)
                              },

            # occurrences second most played
            "OSMP_SUPPORT_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                           role=leaderboards.Role.SUPPORT,
                                                                           region=leaderboards.Region.AMERICAS,
                                                                           mostPlayedSlot=2)
                                      },
            "OSMP_SUPPORT_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                         role=leaderboards.Role.SUPPORT,
                                                                         region=leaderboards.Region.EUROPE,
                                                                         mostPlayedSlot=2)
                                    },
            "OSMP_SUPPORT_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                       role=leaderboards.Role.SUPPORT,
                                                                       region=leaderboards.Region.ASIA,
                                                                       mostPlayedSlot=2)
                                  },
            "OSMP_DAMAGE_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                          role=leaderboards.Role.DAMAGE,
                                                                          region=leaderboards.Region.AMERICAS,
                                                                          mostPlayedSlot=2)
                                     },
            "OSMP_DAMAGE_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                        role=leaderboards.Role.DAMAGE,
                                                                        region=leaderboards.Region.EUROPE,
                                                                        mostPlayedSlot=2)
                                   },
            "OSMP_DAMAGE_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.DAMAGE,
                                                                      region=leaderboards.Region.ASIA,
                                                                      mostPlayedSlot=2)
                                 },
            "OSMP_TANK_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                        role=leaderboards.Role.TANK,
                                                                        region=leaderboards.Region.AMERICAS,
                                                                        mostPlayedSlot=2)
                                   },
            "OSMP_TANK_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.TANK,
                                                                      region=leaderboards.Region.EUROPE,
                                                                      mostPlayedSlot=2)
                                 },
            "OSMP_TANK_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                    role=leaderboards.Role.TANK,
                                                                    region=leaderboards.Region.ASIA,
                                                                    mostPlayedSlot=2)
                               },
            "OSMP_SUPPORT_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.SUPPORT,
                                                                      region=leaderboards.Region.ALL,
                                                                      mostPlayedSlot=2)
                                 },
            "OSMP_DAMAGE_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                     role=leaderboards.Role.DAMAGE,
                                                                     region=leaderboards.Region.ALL,
                                                                     mostPlayedSlot=2)
                                },
            "OSMP_TANK_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                   role=leaderboards.Role.TANK,
                                                                   region=leaderboards.Region.ALL,
                                                                   mostPlayedSlot=2)
                              },

            # occurrences third most played
            "OTMP_SUPPORT_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                           role=leaderboards.Role.SUPPORT,
                                                                           region=leaderboards.Region.AMERICAS,
                                                                           mostPlayedSlot=3
                                                                           )
                                      },
            "OTMP_SUPPORT_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                         role=leaderboards.Role.SUPPORT,
                                                                         region=leaderboards.Region.EUROPE,
                                                                         mostPlayedSlot=3
                                                                         )
                                    },
            "OTMP_SUPPORT_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                       role=leaderboards.Role.SUPPORT,
                                                                       region=leaderboards.Region.ASIA,
                                                                       mostPlayedSlot=3
                                                                       )
                                  },
            "OTMP_DAMAGE_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                          role=leaderboards.Role.DAMAGE,
                                                                          region=leaderboards.Region.AMERICAS,
                                                                          mostPlayedSlot=3
                                                                          )
                                     },
            "OTMP_DAMAGE_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                        role=leaderboards.Role.DAMAGE,
                                                                        region=leaderboards.Region.EUROPE,
                                                                        mostPlayedSlot=3
                                                                        )
                                   },
            "OTMP_DAMAGE_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.DAMAGE,
                                                                      region=leaderboards.Region.ASIA,
                                                                      mostPlayedSlot=3
                                                                      )
                                 },
            "OTMP_TANK_AMERICAS": {"graph": get_occurrences_most_played(data=dataset,
                                                                        role=leaderboards.Role.TANK,
                                                                        region=leaderboards.Region.AMERICAS,
                                                                        mostPlayedSlot=3
                                                                        )
                                   },
            "OTMP_TANK_EUROPE": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.TANK,
                                                                      region=leaderboards.Region.EUROPE,
                                                                      mostPlayedSlot=3
                                                                      )
                                 },
            "OTMP_TANK_ASIA": {"graph": get_occurrences_most_played(data=dataset,
                                                                    role=leaderboards.Role.TANK,
                                                                    region=leaderboards.Region.ASIA,
                                                                    mostPlayedSlot=3
                                                                    )
                               },
            "OTMP_SUPPORT_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                      role=leaderboards.Role.SUPPORT,
                                                                      region=leaderboards.Region.ALL,
                                                                      mostPlayedSlot=3
                                                                      )
                                 },
            "OTMP_DAMAGE_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                     role=leaderboards.Role.DAMAGE,
                                                                     region=leaderboards.Region.ALL,
                                                                     mostPlayedSlot=3
                                                                     )
                                },
            "OTMP_TANK_ALL": {"graph": get_occurrences_most_played(data=dataset,
                                                                   role=leaderboards.Role.TANK,
                                                                   region=leaderboards.Region.ALL,
                                                                   mostPlayedSlot=3
                                                                   )
                              },

            "O_ALL_AMERICAS": {"graph": get_occurrences(data=dataset,
                                                        region=leaderboards.Region.AMERICAS)},
            "O_ALL_EUROPE": {"graph": get_occurrences(data=dataset,
                                                      region=leaderboards.Region.EUROPE)},
            "O_ALL_ASIA": {"graph": get_occurrences(data=dataset,
                                                    region=leaderboards.Region.ASIA)},
            "O_ALL_ALL": {"graph": get_occurrences(data=dataset,
                                                   region=leaderboards.Region.ALL)},


            "MISC": {
                "OHP": get_number_of_ohp(dataset),
                "THP": get_number_of_thp(dataset)
            }
        }
        for key, val in data[s].items():

            if key != "MISC":
                graphData = data[s][key]["graph"]
                data[s][key]["statistic"] = {
                    "mean": round(get_mean(graphData), 3),
                    "variance": round(get_variance(graphData), 3),
                    "standard_deviation": round(get_stdev(graphData), 3)
                }
                data[s][key] = json.dumps(val)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

calculate()


@app.get("/season/{season_number}")
async def season(request: Request, season_number: str):
    global hits
    if season_number in seasons:
        hits += 1
        print(hits)
        return templates.TemplateResponse(
            "index.html",
            {"request": request,
             "seasons": seasons,
             "currentSeason": season_number,
             **data[season_number],
             **data[season_number]["MISC"]}
        )
    return RedirectResponse(f"/season{seasons[-1]}")


@app.get("/{_}")
@app.get("/")
async def index_redirect(request: Request):
    if "favicon.ico" in str(request.url):
        return
    return RedirectResponse(f"/season/{seasons[-1]}")


@app.get("/i/hits", response_class=JSONResponse)
async def hit_endpoint():
    return {"hits": hits}


@app.get("/trends/seasonal")
async def trendsEndpoint(request: Request):
    return templates.TemplateResponse("trends.html",
                                      {"request": request, "seasons": seasons, "trends": json.dumps(trends)})
