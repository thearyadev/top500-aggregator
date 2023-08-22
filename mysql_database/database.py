import datetime
import threading

from mysql.connector import pooling

import leaderboards
from heroes import Hero

lock = threading.Lock()


class DatabaseAccess:
    def __init__(
        self, user: str, password: str, host: str, port: str | int, database: str
    ):
        self.con_pool = pooling.MySQLConnectionPool(
            pool_name="pool",
            pool_size=5,
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        self.dbname = database

    def create_info_table(self):
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE season_info (
                    id VARCHAR(25) PRIMARY KEY NOT NULL,
                    disclaimer VARCHAR(999),
                    patch_notes VARCHAR(999)
                );
                """
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
            lock.release()

    def add_info_entry(
        self, season_identifier: str, disclaimer: str | None, patch_notes: str | None
    ):
        """Adds a new entry to the season_info table in the database

        Args:
            season_identifier (str): season number identifier. Format: season_{seasonNumber}_{subseasonNumber}
            disclaimer (str): disclaimer for the season
            patch_notes (str): patch notes for the season
        """
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO season_info (id, disclaimer, patch_notes) VALUES(%s, %s, %s)",
                (season_identifier, disclaimer, patch_notes),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
            lock.release()

    def create_season(self, seasonNumber: str):
        """Creates a new season table in the database

        Args:
            seasonNumber (str): season number identifier. Format: season_{seasonNumber}_{subseasonNumber}
        """
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"""CREATE TABLE season_{seasonNumber} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    region TEXT,
                    role TEXT,
                    gamesPlayed INT,
                    firstMostPlayed TEXT,
                    secondMostPlayed TEXT,
                    thirdMostPlayed TEXT
                );
                """
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
            lock.release()

    def add_leaderboard_entry(
        self, seasonNumber: str, leaderboard_entry: leaderboards.LeaderboardEntry
    ):
        """adds leaderboard entry to the database for a single season

        Args:
            seasonNumber (str): season number identifier. Format: season_{seasonNumber}_{subseasonNumber}
            leaderboard_entry (leaderboards.LeaderboardEntry): leaderboard entry to add to the database
        """
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"""
            INSERT INTO season_{seasonNumber} 
            (region, role, gamesPlayed, firstMostPlayed, secondMostPlayed, thirdMostPlayed)
            VALUES(%s, %s, %s, %s, %s, %s)
            """,
                (
                    leaderboard_entry.region.name,
                    leaderboard_entry.role.name,
                    leaderboard_entry.games,
                    # can be string or Hero object. If it's a Hero object, get the name.
                    leaderboard_entry.heroes[0].name
                    if isinstance(leaderboard_entry.heroes[0], Hero)
                    else leaderboard_entry.heroes[0],
                    leaderboard_entry.heroes[1].name
                    if isinstance(leaderboard_entry.heroes[1], Hero)
                    else leaderboard_entry.heroes[1],
                    leaderboard_entry.heroes[2].name
                    if isinstance(leaderboard_entry.heroes[2], Hero)
                    else leaderboard_entry.heroes[2],
                ),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
            lock.release()

    def get_all_records(self, seasonNumber: str) -> list[leaderboards.LeaderboardEntry]:
        """_summary_

        Args:
            seasonNumber (str): season number identifier. Format: season_{seasonNumber}_{subseasonNumber}


        Returns:
            list[leaderboards.LeaderboardEntry]: list of leaderboardEntry objects
        """
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT * FROM season_{seasonNumber}",
            )
            data: list[tuple[str, str, str, int, str, str, str]] = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
            lock.release()

        results = list()
        for line in data:
            results.append(
                leaderboards.LeaderboardEntry(
                    heroes=[
                        line[4],  # fmp
                        line[5],  # smp
                        line[6],  # tmp
                    ],
                    role=leaderboards.Role[line[2]],
                    region=leaderboards.Region[line[1]],
                    games=line[3],
                )
            )
        return results

    def get_seasons(self) -> list[str]:
        """Returns a list of all seasons in the database

        Returns:
            list[str]: list of season identifiers. Format: {seasonNumber}_{subseasonNumber}
        """
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM season_info")
            data: list[tuple[str, int]] = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
            lock.release()

        # filter and sort and some other stuff lol.
        seasons_sorted = sorted(
            [entry[0].replace("season_", "") for entry in data],
            key=lambda x: (int(x.split("_")[0]), int(x.split("_")[1])),
        )
        output_seasons = list()
        for season in seasons_sorted:
            if season in ("34_8", "35_8", "36_8"):
                output_seasons.append(season)

        for season in seasons_sorted:
            if season not in ("34_8", "35_8", "36_8"):
                output_seasons.append(season)

        return output_seasons

    def get_total_hero_occurrence_count(
        self, hero: str, region: leaderboards.Region, seasonNumber: str
    ) -> int:
        """Gets the total number of times a hero has appeared in a season

        Args:
            hero (str): hero name
            region (leaderboards.Region): region
            seasonNumber (str): season number identifier. Format: {seasonNumber}_{subseasonNumber}

        Returns:
            int: number of times the hero has appeared in the season
        """
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"""
            SELECT COUNT(*) FROM season_{seasonNumber}
                WHERE region = '{region.name}'
                    AND (
                    firstMostPlayed = '{hero}' OR secondMostPlayed = '{hero}' OR thirdMostPlayed = '{hero}'
                    )
            """,
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
            lock.release()
        result: tuple[int] = self.cursor.fetchone()
        return result[0]

    def get_season_disclaimer(self, seasonNumber: str) -> str:
        """Gets the disclaimer for a season

        Args:
            seasonNumber (str): season number identifier. Format: {seasonNumber}_{subseasonNumber}

        Returns:
            str: disclaimer
        """
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT disclaimer FROM season_info WHERE id = 'season_{seasonNumber}'",
            )
            result: tuple[str] = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()
            lock.release()
        return result[0]

    def add_season_info_entry(
        self, season_identifier: str, disclaimer: str | None, patch_notes: str | None
    ) -> None:
        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO season_info (id, disclaimer, patch_notes) VALUES(?, ?, ?)",
                (season_identifier, disclaimer, patch_notes),
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
            lock.release()
        return None

    def drop_and_rebuild_testing_db(self):
        """Drops the testing database. Only use for testing purposes."""
        if self.dbname == "railway":
            raise ValueError("Cannot drop railway database")

        lock.acquire()
        try:
            connection = self.con_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE {self.dbname}")
            connection.commit()
            cursor.execute(f"CREATE DATABASE {self.dbname}")
            connection.commit()
            cursor.execute(f"USE {self.dbname}")
        finally:
            cursor.close()
            connection.close()
            lock.release()
