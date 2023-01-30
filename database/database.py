import sqlite3
import leaderboards
import threading

lock = threading.Lock()


class DatabaseAccess:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_season(self, seasonNumber: int):
        self.cursor.execute(f"""CREATE TABLE season{seasonNumber}(
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

    def add_leaderboard_entry(self, seasonNumber: int, leaderboard_entry: leaderboards.LeaderboardEntry):
        lock.acquire()
        self.cursor.execute(
            f"""
            INSERT INTO season{seasonNumber} 
            (region, role, gamesPlayed, firstMostPlayed, secondMostPlayed, thirdMostPlayed)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (leaderboard_entry.region, leaderboard_entry.role, leaderboard_entry.games,
             leaderboard_entry.heroes[0].name, leaderboard_entry.heroes[1].name, leaderboard_entry.heroes[2].name,)
        )
        self.connection.commit()
        lock.release()

    def get_all_records(self, seasonNumber: int) -> list[leaderboards.LeaderboardEntry]:
        lock.acquire()
        self.cursor.execute(f"SELECT * FROM season{seasonNumber}")
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

    def get_seasons(self) -> list[int]:
        lock.acquire()
        results: list[int] = list()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = self.cursor.fetchall()
        lock.release()
        for t in tables:
            val: str = t[0][-1]
            if val.isdigit():
                results.append(int(val))
        return results


if __name__ == '__main__':
    dba = DatabaseAccess("../data/data.db")
