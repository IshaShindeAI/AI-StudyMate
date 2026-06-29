from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")

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

        message = data.get("message")

        if not message:
            return jsonify({
                "error": "No message received"
            }), 400


        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )


        return jsonify({
            "reply": response.choices[0].message.content
        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500