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

# Track user progress and state (in-memory, resets if app restarts)
user_state = {}  # Tracks where the user is in the flow: 'start', 'toc', 'lesson', etc.

@app.route('/')
def home():
    return 'WhatsApp 5-Minute Daily Lesson Assistant is running!'

# Webhook route for incoming WhatsApp messages
@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    sender = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').strip().lower()

    # Default state is 'start' if user is new
    state = user_state.get(sender, 'start')
    reply = ""

    if state == 'start':
        # Greet and ask if user wants to start
        reply = ("Hello! 👋 This is your 5-minute lesson assistant. "
                 "Would you like to start learning?\n\n"
                 "Reply with 'yes' to see the table of contents, or 'no' to exit.")
        user_state[sender] = 'awaiting_yes_no'

    elif state == 'awaiting_yes_no':
        if incoming_msg == 'yes':
            # Show table of contents
            toc = "Here are the available lessons:\n"
            for i, lesson in enumerate(lessons, 1):
                title = lesson.split(".\n\n")[0]
                toc += f"{i}. {title}\n"
            toc += "\nReply with the number of the lesson you'd like to explore."
            reply = toc
            user_state[sender] = 'awaiting_lesson_choice'
        elif incoming_msg == 'no':
            reply = ("No problem! If you change your mind, just say 'hi' or 'start' anytime to begin learning. Have a great day! 😊")
            user_state[sender] = 'start'  # Reset state
        else:
            reply = ("Please reply with 'yes' to see the table of contents, or 'no' to exit.")

    elif state == 'awaiting_lesson_choice':
        if incoming_msg.isdigit():
            lesson_num = int(incoming_msg)
            if 1 <= lesson_num <= len(lessons):
                reply = lessons[lesson_num - 1] + "\n\nReply 'menu' to see the table of contents again, or 'exit' to end."
                user_state[sender] = 'in_lesson'
            else:
                reply = f"Please reply with a number between 1 and {len(lessons)} to choose a lesson."
        else:
            reply = f"Please reply with the number of the lesson you'd like to explore."

    elif state == 'in_lesson':
        if incoming_msg == 'menu':
            toc = "Here are the available lessons:\n"
            for i, lesson in enumerate(lessons, 1):
                title = lesson.split(".\n\n")[0]
                toc += f"{i}. {title}\n"
            toc += "\nReply with the number of the lesson you'd like to explore."
            reply = toc
            user_state[sender] = 'awaiting_lesson_choice'
        elif incoming_msg == 'exit':
            reply = ("Thank you for learning with me! If you want to start again, just say 'hi' or 'start'. Have a wonderful day! 🌟")
            user_state[sender] = 'start'
        else:
            reply = ("Reply 'menu' to see the table of contents again, or 'exit' to end.")
    else:
        # Fallback for any unexpected state
        reply = ("Hello! 👋 This is your 5-minute lesson assistant. Would you like to start learning?\n\nReply with 'yes' to see the table of contents, or 'no' to exit.")
        user_state[sender] = 'awaiting_yes_no'

    # Create a Twilio response object
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)

    return str(resp)

# TODO: Add WhatsApp webhook route for Twilio integration
# TODO: Add user registration and lesson delivery logic

if __name__ == '__main__':
    app.run(debug=True) 