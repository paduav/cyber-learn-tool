# formatter.py

from db_app.models import get_ranked_activities

def prepare_activities_for_ai(topic, difficulty, time, standards):
    activities = get_ranked_activities(topic, difficulty, time, standards)

    if not activities:
        return None

    return format_for_ai(activities)

def format_for_ai(activities):
    formatted = "Here are some cybersecurity lessons ranked by relevance:\n\n"

    for i, a in enumerate(activities, 1):
        if a['max_time_minutes'] is not None:
            time_str = f"{a['min_time_minutes']}–{a['max_time_minutes']} minutes"
        else:
            time_str = f"{a['min_time_minutes']} minutes"

        formatted += (
            f"Activity {i} (Relevance Score: {a['score']}):\n"
            f"Title: {a['title']}\n"
            f"Topic: {a['topic']}\n"
            f"Learning Objectives: {a['learning_objectives']}\n"
            f"Time: {time_str}\n"
            f"Materials: {a['materials']}\n"
            f"Difficulty: {a['difficulty']}\n"
            f"Standards: {a.get('standards') or 'N/A'}\n"
            f"Tags: {a['tags']}\n"
            f"Link: {a['link']}\n\n"
        )

    return formatted

