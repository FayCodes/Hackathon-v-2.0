from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
DAILY_LESSON_SECRET = os.getenv('DAILY_LESSON_SECRET', 'changeme')

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
USER_PROGRESS_FILE = 'user_progress.json'

# Load user progress from file at startup
try:
    with open(USER_PROGRESS_FILE, 'r') as f:
        user_progress = {k: set(v) for k, v in json.load(f).items()}
except (FileNotFoundError, json.JSONDecodeError):
    user_progress = {}

# Helper to save user progress to file
def save_user_progress():
    with open(USER_PROGRESS_FILE, 'w') as f:
        # Convert sets to lists for JSON serialization
        json.dump({k: list(v) for k, v in user_progress.items()}, f)

CERTIFICATE_MESSAGE = (
    "🎉 Congratulations! 🎉\n\n"
    "You have completed all available lessons in the WhatsApp 5-Minute Daily Lesson Assistant.\n"
    "This is your digital certificate of completion.\n\n"
    "Keep learning and growing!\n\n"
    "If you'd like to receive this certificate again, reply 'certificate'."
)

# Helper to send WhatsApp message via Twilio
def send_whatsapp_message(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=body,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to
    )

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
    completed = user_progress.get(sender, set())
    reply = ""

    # --- New: Handle 'certificate' command from any state ---
    if incoming_msg == 'certificate':
        if len(completed) == len(lessons) and len(lessons) > 0:
            reply = CERTIFICATE_MESSAGE
        else:
            reply = "You need to complete all lessons to receive your certificate! Keep going!"
    # --- Existing: Handle 'help' and 'progress' commands from any state ---
    elif incoming_msg == 'help':
        reply = (
            "Here are some things you can do:\n"
            "- Say 'yes' to start learning or see the table of contents.\n"
            "- Reply with a lesson number to view that lesson.\n"
            "- Reply 'menu' to see the table of contents again.\n"
            "- Reply 'progress' to see your learning progress.\n"
            "- Reply 'certificate' to receive your certificate (after completing all lessons).\n"
            "- Reply 'exit' to end the session.\n"
            "- Say 'hi' or 'start' to begin again anytime."
        )
    elif incoming_msg == 'progress':
        if completed:
            completed_list = sorted(list(completed))
            completed_titles = [lessons[i-1].split(".\n\n")[0] for i in completed_list]
            completed_str = '\n'.join([f"{i}. {title}" for i, title in zip(completed_list, completed_titles)])
            if len(completed) == len(lessons):
                reply = (
                    f"You have completed ALL {len(lessons)} lessons!\n"
                    f"{completed_str}\n\n"
                    "Reply 'certificate' to receive your digital certificate."
                )
            else:
                reply = (
                    f"You have completed {len(completed)} out of {len(lessons)} lessons:\n"
                    f"{completed_str}\n\n"
                    "Keep going! Reply 'menu' to see the table of contents or a lesson number to continue."
                )
        else:
            reply = (
                "You haven't completed any lessons yet.\n"
                "Reply 'menu' to see the table of contents and start learning!"
            )
    else:
        if state == 'start':
            # Greet and show progress if returning user
            if completed:
                reply = (f"Welcome back! 👋 You have completed {len(completed)} out of {len(lessons)} lessons. "
                         "Would you like to continue learning?\n\n"
                         "Reply with 'yes' to see the table of contents, or 'no' to exit.")
            else:
                reply = ("Hello! 👋 This is your 5-minute lesson assistant. "
                         "Would you like to start learning?\n\n"
                         "Reply with 'yes' to see the table of contents, or 'no' to exit.")
            user_state[sender] = 'awaiting_yes_no'

        elif state == 'awaiting_yes_no':
            if incoming_msg == 'yes':
                # Show table of contents with progress
                toc = "Here are the available lessons:\n"
                for i, lesson in enumerate(lessons, 1):
                    title = lesson.split(".\n\n")[0]
                    check = "✅" if i in completed else ""
                    toc += f"{i}. {title} {check}\n"
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
                    # Mark lesson as completed
                    completed = user_progress.get(sender, set())
                    completed.add(lesson_num)
                    user_progress[sender] = completed
                    save_user_progress()  # Save progress to file
                    # If this was the last lesson, send certificate message
                    if len(completed) == len(lessons):
                        reply = lessons[lesson_num - 1] + "\n\n" + CERTIFICATE_MESSAGE
                    else:
                        reply = lessons[lesson_num - 1] + "\n\nReply 'menu' to see the table of contents again, or 'exit' to end."
                    user_state[sender] = 'in_lesson'
                else:
                    reply = f"Please reply with a number between 1 and {len(lessons)} to choose a lesson."
            else:
                reply = f"Please reply with the number of the lesson you'd like to explore."

        elif state == 'in_lesson':
            if incoming_msg == 'menu':
                toc = "Here are the available lessons:\n"
                completed = user_progress.get(sender, set())
                for i, lesson in enumerate(lessons, 1):
                    title = lesson.split(".\n\n")[0]
                    check = "✅" if i in completed else ""
                    toc += f"{i}. {title} {check}\n"
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

# Endpoint for Zapier to trigger daily lesson delivery
@app.route('/send-daily-lessons', methods=['POST'])
def send_daily_lessons():
    # Check secret key in request (header or form)
    secret = request.headers.get('X-DAILY-SECRET') or request.form.get('secret')
    if secret != DAILY_LESSON_SECRET:
        return 'Unauthorized', 401

    sent_count = 0
    for user, completed in user_progress.items():
        # Find the next uncompleted lesson
        next_lesson = None
        for i in range(1, len(lessons)+1):
            if i not in completed:
                next_lesson = i
                break
        if next_lesson:
            # Mark as completed and save
            completed.add(next_lesson)
            user_progress[user] = completed
            save_user_progress()
            # Send the lesson
            send_whatsapp_message(user, f"Your daily lesson:\n\n" + lessons[next_lesson-1] + "\n\nReply 'menu' to see all lessons or 'progress' to check your progress.")
            sent_count += 1
        elif len(completed) == len(lessons):
            # All lessons completed, optionally send certificate
            send_whatsapp_message(user, CERTIFICATE_MESSAGE)
    return f"Sent daily lessons to {sent_count} users.", 200

# TODO: Add WhatsApp webhook route for Twilio integration
# TODO: Add user registration and lesson delivery logic

if __name__ == '__main__':
    app.run(debug=True) 