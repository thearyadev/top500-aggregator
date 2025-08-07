import sys
from PIL import Image

sys.path.append("./")  # used to import from root directory

import leaderboards

R = leaderboards.parse_leaderboard_to_leaderboard_entries(  # parse leaderboard
                leaderboard_image=Image.open("./assets/benchmark/TANK_S17_P24_ASIA/LB-IMG.png"),
                region=leaderboards.Region.AMERICAS,  # doesnt matter
                role=leaderboards.Role.DAMAGE,  # doesnt matter
            )
import json
x = {"answers": []}
for i in R:
    x["answers"].append(i.heroes)
print(x)
print(json.dumps(x))
