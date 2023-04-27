import sqlite3

conn = sqlite3.connect("./data/data.db")
cur = conn.cursor()

cur.execute("SELECT * FROM season_info")
seasons: list[str] = [s[0] for s in cur.fetchall()]
for season in seasons: 
    cur.execute(f"""
    UPDATE {season} SET firstMostPlayed = "Blank" WHERE firstMostPlayed = "Blank2";
    """)
    cur.execute(f"""
    UPDATE {season} SET secondMostPlayed = "Blank" WHERE secondMostPlayed = "Blank2";
    """)
    cur.execute(f"""
    UPDATE {season} SET thirdMostPlayed = "Blank" WHERE thirdMostPlayed = "Blank2";
    """)
    conn.commit()
conn.close()