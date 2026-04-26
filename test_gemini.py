import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API key not found")
    exit()

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