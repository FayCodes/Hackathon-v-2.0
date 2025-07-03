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

# Sample lessons (replace with your own content!)
lessons = [
    "Lesson 1: Introduction to Digital Skills. Today, let's learn what digital skills are and why they're important!",
    "Lesson 2: Basic Email Skills. Learn how to create, send, and reply to emails professionally.",
    "Lesson 3: Using Search Engines. Tips for finding information quickly and safely online.",
    "Lesson 4: Introduction to Microsoft Word. Learn how to create and format simple documents.",
    "Lesson 5: Staying Safe Online. Understand the basics of online privacy and security."
]

# Track user progress (in-memory, resets if app restarts)
user_progress = {}

@app.route('/')
def home():
    return 'WhatsApp 5-Minute Daily Lesson Assistant is running!'

# Webhook route for incoming WhatsApp messages
@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    sender = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').strip().lower()

    # Get user's current lesson index, default to 0
    idx = user_progress.get(sender, 0)

    # If user sends 'next', go to next lesson
    if incoming_msg == 'next':
        idx += 1

    # If out of lessons, send a completion message
    if idx >= len(lessons):
        reply = "Congratulations! You've completed all available lessons. More coming soon!"
    else:
        reply = lessons[idx]
        user_progress[sender] = idx  # Save progress

    # Create a Twilio response object
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)

    return str(resp)

# TODO: Add WhatsApp webhook route for Twilio integration
# TODO: Add user registration and lesson delivery logic

if __name__ == '__main__':
    app.run(debug=True) 