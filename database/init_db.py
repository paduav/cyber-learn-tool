# database/init_db.py


import sqlite3
import os

DB_PATH = "activities.db"

def init_db():
    # delete old DB (for testing)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        topic TEXT NOT NULL,
        learning_objectives TEXT,
        standards TEXT,
        materials TEXT,
        min_time_minutes INTEGER NOT NULL,
        max_time_minutes INTEGER,
        difficulty TEXT,
        activity_type TEXT,
        tags TEXT,
        link TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")

if __name__ == "__main__":
    init_db()