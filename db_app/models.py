import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "activities.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_ranked_activities(topic, difficulty, time, standards):
    conn = get_connection()
    cursor = conn.cursor()

    # filter relevant activities
    #WHERE topic = ? OR tags LIKE ?
    #, (topic, f"%{topic}%")
    cursor.execute("""
        SELECT * FROM activities
        """)
    rows = cursor.fetchall()
    conn.close()

    activities = []

    for row in rows:
        activity = {
            "id": row[0],
            "title": row[1],
            "topic": row[2],
            "learning_objectives": row[3],
            "standards": row[4],
            "materials": row[5],
            "min_time_minutes": row[6],
            "max_time_minutes": row[7],
            "difficulty": row[8],
            "activity_type": row[9],
            "tags": row[10],
            "link":row[11]
        }

        score = 0

        # topic match
        topic_values = normalize_filters(topic)
        standard_values = normalize_filters(standards)

        if any(value.lower() == (activity["topic"] or "").lower() for value in topic_values):
            score += 3

        # difficulty match
        if difficulty == activity["difficulty"]:
            score += 2

        # time match
        min_time = activity["min_time_minutes"]
        max_time = activity["max_time_minutes"]

        if min_time is not None and max_time is not None:
            if min_time <= time <= max_time:
                score += 2

        # standards match
        if standard_values and activity["standards"]:
            if any(value.lower() in activity["standards"].lower() for value in standard_values):
                score += 3

        # tag match
        tags = (activity["tags"] or "").lower()
        if any(value.lower() in tags for value in topic_values):
            score += 1

        activity["score"] = score
        activities.append(activity)

    activities.sort(key=lambda x: x["score"], reverse=True)

    # return all activities ranked. To return top (3) activities, append [:3]
    return activities[:46]

def normalize_filters(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, str) and value.strip():
        return [value.strip()]

    return []
