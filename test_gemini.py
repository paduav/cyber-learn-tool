import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    print("ERROR: Gemini SDK is not installed. Run `python3 -m pip install -r requirements.txt`.")
    raise SystemExit(1)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY is not set.")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

user_prompt = input("Enter a prompt: " + "")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt
    )

    print("\n=== AI RESPONSE ===\n")
    print(response.text)

except Exception as e:
    print("Error:", e)
