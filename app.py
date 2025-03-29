from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
from google.cloud.dialogflow_v2.types import TextInput, QueryInput

app = Flask(__name__)

# Load credentials from the JSON key file
credentials = service_account.Credentials.from_service_account_file("credentials.json")

# Dialogflow project details
DIALOGFLOW_PROJECT_ID = "mahila-mitra-umby"  # Replace with actual project ID

# Function to communicate with Dialogflow
def detect_intent(text):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = f"projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/unique-session-id"

    text_input = TextInput(text=text, language_code="en")
    query_input = QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text

# API endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        bot_reply = detect_intent(user_message)
        return jsonify({"response": bot_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Home route to check if Flask is running
@app.route('/')
def home():
    return "Welcome to the Mahila Mitra Chatbot API!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
