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


if __name__ == '__main__':
    dba = DatabaseAccess("../data/data.db")
