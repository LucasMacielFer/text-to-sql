import google.generativeai as genai

def connect_gemini(api_key):
    if api_key is None:
        raise ValueError("The environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    return model

def start_chat(model, context):
    initial_context = [
        {
            "role": "user",
            "parts": ["You are an SQL expert. Your task is to receive requests in natural language "\
            "and translate them into an SQL query. Return ONLY the SQL query code, without any explanation, "\
            "introduction, or markdown formatting like ```sql. All your outputs will be executed directly "\
            "in a terminal. The database context is the following: " + context
            ]
        },
        {
            "role": "model",
            "parts": ["Entendido. Estou pronto para receber os pedidos e gerar as consultas SQL."]
        },
    ]

    chat = model.start_chat(history=initial_context)
    return chat

def generate_query(search, chat):
    if search.lower() not in ["exit", "quit", "q", "\q", "leave"]:
        prompt = search
        prompt += "Return ONLY the SQL query, as its going directly into the terminal."
        answer = chat.send_message(prompt)
        query = answer.text[6:-3]
    else:
        query = None
    return query