import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from db_app.formatter import prepare_activities_for_ai

load_dotenv()


def normalize_request_list(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, str) and value.strip():
        return [value.strip()]

    return []


def get_genai_client():
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "Gemini SDK is not installed. Run `python3 -m pip install -r requirements.txt` "
            "from the project folder."
        ) from exc

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your environment or `.env` file."
        )

    return genai.Client(api_key=api_key)

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/lesson-plan")
    def lesson_plan_page():
        return render_template("lesson-plan.html")

    @app.route("/generate-lesson-plan", methods=["POST"])
    def generate_lesson_plan():
        try:
            client = get_genai_client()
            data = request.get_json()

            topic = normalize_request_list(data.get("topic"))
            difficulty = data.get("difficultyLevel")
            duration = data.get("duration", {}).get("totalMinutes")
            standards = normalize_request_list(data.get("standardsAlignment"))
            customization = data.get("additionalCustomization")

            activities = prepare_activities_for_ai(
                topic, difficulty, duration, standards
            )

            topic_display = ", ".join(topic) if topic else "N/A"
            standards_display = ", ".join(standards) if standards else "N/A"

            prompt = f"""
You are an expert curriculum designer for middle school cybersecurity education.

Please use the following user inputs:
- Topic: {topic_display}
- Difficulty Level: {difficulty}
- Time Allotment: {duration} minutes
- Standards: {standards_display}
- Additional Comments: {customization}

Here are relevant activities from the database:
{activities}

TASK:
1. Select appropriate activities from the database.
2. Create a structured lesson plan.
3. Follow this EXACT JSON format:

{{
  "title": "...",
  "summary": "...",
  "tags": [...],
  "learningObjectives": [...],
  "standardsAlignment": [...],
  "materials": [...],
  "introduction": {{
    "time": "...",
    "text": "...",
    "bullets": [...]
  }},
  "activities": [
    {{
      "title": "...",
      "time": "...",
      "text": "...",
      "bullets": [...]
    }}
  ],
  "discussionReflection": {{
    "time": "...",
    "bullets": [...]
  }},
  "wrapUp": {{
    "time": "...",
    "text": "...",
    "note": "..."
  }}
}}

IMPORTANT:
- ONLY return valid JSON
- Do NOT include markdown or explanations
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            import json

            cleaned = response.text.strip()

            cleaned = cleaned.replace("```json", "").replace("```", "")

            lesson_plan = json.loads(cleaned)

            return jsonify(lesson_plan)

        except Exception as e:
            print("ERROR:", e)
            return jsonify({"error": str(e)}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
