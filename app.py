from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "AI StudyMate is running!"


@app.route("/chat", methods=["POST"])
def chat():

    try:

        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            return jsonify({
                "error": "GROQ_API_KEY is missing in Vercel"
            }), 500


        client = Groq(
            api_key=api_key
        )


        data = request.get_json()

        message = data.get("message")


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

        return jsonify({
            "error": str(e)
        }), 500