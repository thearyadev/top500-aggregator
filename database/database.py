import sqlite3
import leaderboards
import threading

lock = threading.Lock()


class DatabaseAccess:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_season(self, seasonNumber: str):
        self.cursor.execute(f"""CREATE TABLE season_{seasonNumber}(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    region TEXT,
                                    role TEXT,
                                    gamesPlayed INTEGER,
                                    firstMostPlayed TEXT,
                                    secondMostPlayed TEXT,
                                    thirdMostPlayed TEXT
                            )"""
                            )
        self.connection.commit()

    def add_leaderboard_entry(self, seasonNumber: str, leaderboard_entry: leaderboards.LeaderboardEntry):
        lock.acquire()
        self.cursor.execute(
            f"""
            INSERT INTO season_{seasonNumber} 
            (region, role, gamesPlayed, firstMostPlayed, secondMostPlayed, thirdMostPlayed)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (leaderboard_entry.region, leaderboard_entry.role, leaderboard_entry.games,
             leaderboard_entry.heroes[0].name, leaderboard_entry.heroes[1].name, leaderboard_entry.heroes[2].name,)
        )
        self.connection.commit()
        lock.release()

    def get_all_records(self, seasonNumber: str) -> list[leaderboards.LeaderboardEntry]:
        lock.acquire()
        self.cursor.execute(f"SELECT * FROM season_{seasonNumber}")
        data = self.cursor.fetchall()
        lock.release()
        results = list()
        for line in data:
            results.append(
                leaderboards.LeaderboardEntry(
                    heroes=[line[4], line[5], line[6], ],
                    role=leaderboards.Role[line[2]],
                    region=leaderboards.Region[line[1]],
                    games=line[3]
                )
            )

        return results

    def get_seasons(self) -> list[str]:
        lock.acquire()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = self.cursor.fetchall()
        lock.release()
        return [t[0].replace("season_", "") for t in tables][1:]


if __name__ == '__main__':
    dba = DatabaseAccess("../data/data.db")
