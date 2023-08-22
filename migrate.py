import database
import mysql_database
import mysql.connector
from dotenv import load_dotenv
import os
import statistic
from leaderboards import Region, Role

load_dotenv()

# db = database.DatabaseAccess("./data/data.db")
tdb = mysql_database.DatabaseAccess(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=os.getenv("MYSQLPORT"),
)

# print("migrating")
# for season in db.get_seasons():
#     records = db.get_all_records(season)
#     print(season)
#     for record in records:
#         print(record)
#         tdb.add_leaderboard_entry(
#             seasonNumber=season,
#             leaderboard_entry=record,
#         )

data = []

for season in tdb.get_seasons()[:1]:
    data.append(tdb.get_all_records(seasonNumber=season))

print(len(data))
input("enter to continue")

def test_get_variance():
    for season_data in data:
        for region in [Region.AMERICAS, Region.EUROPE, Region.ASIA]:
            for role in [Role.DAMAGE, Role.SUPPORT, Role.TANK]:
                for most_played_slot in (1, 2, 3):
                    print( statistic.get_variance(
                        data=statistic.get_occurrences_most_played(
                            data=season_data,
                            region=region,
                            role=role,
                            mostPlayedSlot=most_played_slot,
                        )
                    ))

                print (statistic.get_variance(
                    data=statistic.get_occurrences(data=season_data, region=region)
                ))
print(
    statistic.get_occurrences_most_played(
        data=data[0],
        region=Region.AMERICAS,
        role=Role.SUPPORT,
        mostPlayedSlot=1,
    )
)