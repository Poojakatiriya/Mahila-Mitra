import os
from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
from google.cloud.dialogflow_v2.types import TextInput, QueryInput

app = Flask(__name__)

# Load credentials securely
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "secrets/credentials.json")

if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"Missing credentials file: {CREDENTIALS_PATH}. Ensure it's set in the environment.")

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

# Dialogflow project details
DIALOGFLOW_PROJECT_ID = "mahila-mitra-umby"  # Replace with your actual project ID

# Function to communicate with Dialogflow
def detect_intent(text):
    try:
        session_client = dialogflow.SessionsClient(credentials=credentials)
        session = f"projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/unique-session-id"

        text_input = TextInput(text=text, language_code="en")
        query_input = QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text

    except Exception as e:
        return f"Error communicating with Dialogflow: {str(e)}"

# API endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        bot_reply = detect_intent(user_message)
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

# Home route to check if Flask is running
@app.route('/')
def home():
    return "Welcome to the Mahila Mitra Chatbot API!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
