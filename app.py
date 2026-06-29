@app.route("/chat", methods=["POST"])
def chat():

    try:
        api_key = os.environ.get("GROQ_API_KEY")

        return jsonify({
            "api_key_exists": api_key is not None,
            "api_key_length": len(api_key) if api_key else 0
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500