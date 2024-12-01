from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Rasa server URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"


@app.route("/")
def index():
    """
    Render the chatbot UI with a welcome message.
    """
    welcome_message = "Welcome to the Banking Bot! How can I assist you today?"
    return render_template("index.html", welcome_message=welcome_message)

@app.route("/send_message", methods=["POST"])
def send_message():
    """
    Send user message to Rasa and get the bot's response.
    """
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Send the user message to Rasa
    response = requests.post(
        RASA_SERVER_URL,
        json={"sender": "user", "message": user_message}
    )

    if response.status_code == 200:
        rasa_responses = response.json()
        bot_message = " ".join([resp.get("text", "") for resp in rasa_responses])
        return jsonify({"bot_message": bot_message})
    else:
        return jsonify({"error": "Failed to get a response from the Rasa server"}), 500

if __name__ == "__main__":
    app.run(debug=True)
