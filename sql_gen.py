import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_KEY")

if api_key is None:
    raise ValueError("A The environment variable is not set.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.0-flash")

pergunta = input("Digite: ")
response = model.generate_content(pergunta)
print("\n")
print(response.text)