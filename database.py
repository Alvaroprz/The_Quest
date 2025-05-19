
import sqlite3

DB_NAME = "records.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS scores (initials TEXT, score INTEGER)")
    conn.commit()
    conn.close()

def save_score(initials, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO scores (initials, score) VALUES (?, ?)", (initials, score))
    conn.commit()
    conn.close()

def get_top_scores():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT initials, score FROM scores ORDER BY score DESC LIMIT 5")
    scores = c.fetchall()
    conn.close()
    return scores
