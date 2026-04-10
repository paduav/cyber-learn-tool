# formatter.py


from app.models import get_ranked_activities

def prepare_activities_for_ai(topic, difficulty, time, standards):
    activities = get_ranked_activities(topic, difficulty, time, standards)

    if not activities:
        return None

    return format_for_ai(activities)


def format_for_ai(activities):
    formatted = "Here are some activities:\n\n"

    for i, a in enumerate(activities, 1):
        formatted += (
            f"Activity {i}:\n"
            f"Title: {a['title']}\n"
            f"Topic: {a['topic']}\n"
            f"Learning Objectives: {a['learning_objectives']}\n"
            f"Time: {a['min_time_minutes']}–{a['max_time_minutes']} minutes\n"
            f"Materials: {a['materials']}\n"
            f"Difficulty: {a['difficulty']}\n"
            f"Standards: {a.get('standards') or 'N/A'}\n"
            f"Tags: {a['tags']}\n\n"
        )

    return formatted

