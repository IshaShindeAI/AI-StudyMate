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
        # Check if Groq key exists in Vercel
        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            return jsonify({
                "error": "GROQ_API_KEY is missing in Vercel Environment Variables"
            }), 500


        client = Groq(
            api_key=api_key
        )


        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400


        message = data.get("message")

        if not message:
            return jsonify({
                "error": "Message is missing"
            }), 400


        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": "You are AI StudyMate, a helpful study assistant."
                },
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



# Local testing
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=3000
    )