import google.generativeai as genai

def connect_gemini(api_key):
    if api_key is None:
        raise ValueError("The environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    return model

def generate_query(context, search, model):
    if search.lower() not in ["exit", "quit", "q", "\q", "leave"]:
        prompt = context
        prompt += search
        prompt += "Return ONLY the SQL query, as its going directly into the terminal."
        answer = model.generate_content(prompt)
        query = answer.text[6:-3]
    else:
        query = None
    return query