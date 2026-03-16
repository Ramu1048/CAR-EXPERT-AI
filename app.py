from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import json

app = Flask(__name__)

# ---------------- GEMINI API ----------------
genai.configure(api_key="ENTER YOUR API KEY ")

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- CHATBOT HISTORY ----------------
CHAT_FILE = "chat_history.json"

# Create chat history file if it doesn't exist
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump([], f)


def load_chat_history():
    """Load chat history safely; reset file if it is empty/corrupt."""
    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                write_chat_history([])
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        write_chat_history([])
        return []


def write_chat_history(chat_history):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4)

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are a professional automobile expert assistant.

When a user asks about a car model (example: Tesla Model 3, Toyota Innova, Maruti Suzuki Swift),
you must respond in this format:

Car Name:
Manufacturer:

Engine:

Top Speed:

Horsepower:

Torque:

Mileage / Range:

Fuel Type:

Transmission:

Price Range:

Key Features:

Only answer questions related to cars.
If the user asks anything else reply:
"I can only answer questions related to cars."
"""

# ---------------- CAR KEYWORDS ----------------
car_keywords = [
    "car","vehicle","engine","speed","horsepower","torque",
    "maruti","suzuki","toyota","innova","tesla","bmw","audi",
    "honda","hyundai","kia","ford","mahindra","tata",
    "mileage","range","electric","diesel","petrol","model"
]

# ---------------- SAVE CHAT ----------------
def save_chat(user_message, bot_reply):
    chat_history = load_chat_history()

    chat_history.append({
        "user": user_message,
        "bot": bot_reply
    })

    write_chat_history(chat_history)

# ---------------- CHECK IF CAR QUESTION ----------------
def is_car_question(text):
    text = text.lower()
    return any(word in text for word in car_keywords)

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CHAT API ----------------
@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message", "")

    # Check if the question is related to cars
    if not is_car_question(user_message):

        bot_reply = "I can only answer questions related to cars."

        save_chat(user_message, bot_reply)

        return jsonify({"reply": bot_reply})

    try:

        prompt = SYSTEM_PROMPT + "\nUser Question: " + user_message

        response = model.generate_content(prompt)

        bot_reply = response.text

        # Save chat
        save_chat(user_message, bot_reply)

        return jsonify({"reply": bot_reply})

    except Exception as e:

        app.logger.exception("Error generating response")

        return jsonify({
            "error": "Failed to generate response",
            "details": str(e)
        }), 500

# ---------------- GET CHAT HISTORY ----------------
@app.route("/history")
def history():
    return jsonify(load_chat_history())

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
