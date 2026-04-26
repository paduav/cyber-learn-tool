from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from google import genai
from db_app.formatter import prepare_activities_for_ai

load_dotenv()

def create_app():
    app = Flask(__name__)

    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/lesson-plan")
    def lesson_plan_page():
        return render_template("lesson-plan.html")

    @app.route("/generate-lesson-plan", methods=["POST"])
    def generate_lesson_plan():
        try:
            data = request.get_json()

            topic = data.get("topic")
            difficulty = data.get("difficultyLevel")
            duration = data.get("duration", {}).get("totalMinutes")
            standards = data.get("standardsAlignment")
            customization = data.get("additionalCustomization")

            activities = prepare_activities_for_ai(
                topic, difficulty, duration, standards
            )

            prompt = f"""
You are an expert curriculum designer for middle school cybersecurity education.

Please use the following user inputs:
- Topic: {topic}
- Difficulty Level: {difficulty}
- Time Allotment: {duration} minutes
- Standards: {standards}
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