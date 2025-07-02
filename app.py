from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

app = Flask(__name__)

@app.route('/')
def home():
    return 'WhatsApp 5-Minute Daily Lesson Assistant is running!'

# Webhook route for incoming WhatsApp messages
@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    # Create a Twilio response object
    resp = MessagingResponse()
    msg = resp.message()

    # Simple reply for now
    msg.body('Hello! This is your 5-minute lesson assistant. Stay tuned for daily lessons!')

    return str(resp)

# TODO: Add WhatsApp webhook route for Twilio integration
# TODO: Add user registration and lesson delivery logic

if __name__ == '__main__':
    app.run(debug=True) 