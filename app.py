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
    "Lesson 1: Introduction to Digital Skills.\n\nDigital skills are abilities that let you use computers, smartphones, and the internet to solve problems, communicate, and find information. In today's world, digital skills are essential for learning, working, and staying connected. Think about how you use technology every day—sending messages, searching for information, or using apps. These are all examples of digital skills!\n\nTip: Try exploring a new app or website today and see what you can learn.",
    "Lesson 2: Basic Email Skills.\n\nEmail is a key tool for communication in school, work, and daily life. To get started, create a free email account (like Gmail or Yahoo). Practice writing a short, polite message to a friend or family member. Remember to include a subject line and sign your name at the end.\n\nTip: Always check your email for new messages and reply promptly when needed.",
    "Lesson 3: Using Search Engines.\n\nSearch engines like Google help you find information quickly. To search, type a question or keywords into the search bar (e.g., 'how to write a CV'). Look at the top results and check if the information is from a trustworthy source.\n\nTip: Use specific words in your search to get better results, and avoid clicking on suspicious links.",
    "Lesson 4: Introduction to Microsoft Word.\n\nMicrosoft Word is a popular program for creating documents like letters, resumes, and reports. Open Word and try typing a short paragraph. Experiment with changing the font, size, and color of your text.\n\nTip: Save your document often so you don't lose your work!\n\nChallenge: Try creating a simple CV or letter using Word.",
    "Lesson 5: Staying Safe Online.\n\nOnline safety is important. Never share your passwords or personal information with strangers. Be careful about what you post on social media. If you receive a suspicious email or message, don't click on any links—delete it instead.\n\nTip: Use strong passwords and change them regularly.\n\nRemember: If something online makes you uncomfortable, talk to a trusted adult or friend."
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