from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
api_key = os.environ.get("GROQ_API_KEY")

client = Groq(
    api_key=api_key
)


@app.route("/")
def home():
    return "AI StudyMate is running!"


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "error": "Message is required"
            }), 400

        user_message = data["message"]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are AI StudyMate, a helpful study assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Vercel needs this
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)