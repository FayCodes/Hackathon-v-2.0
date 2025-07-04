# WhatsApp 5-Minute Daily Lesson Assistant

## Solution Statement
Many hustlers and students want to learn new skills but don't have time for long courses. This project provides a WhatsApp assistant that delivers 5-minute daily lessons (vocational, English, digital skills, etc.) in a conversational, interactive way. The assistant tracks user progress, awards certificates, and automates daily learning—all through WhatsApp.

## Features
- **WhatsApp Integration:** Users interact with the assistant directly on WhatsApp via Twilio integration.
- **Deployed to the Cloud:** The app is live and accessible via Render.
- **Interactive Conversation Flow:**
  - Friendly greeting and onboarding
  - Table of contents for lessons
  - Users select lessons by number
  - "Help" and "progress" commands for guidance
- **Lesson Content Management:**
  - Detailed, beginner-friendly lessons
  - Easy to expand with more content
- **User Progress Tracking:**
  - Tracks which lessons each user has completed
  - Shows checkmarks for completed lessons
  - Greets returning users with their progress
- **Persistent Storage:**
  - User progress is saved in a JSON file for reliability
- **Digital Certificate:**
  - Users receive a congratulatory certificate message upon completing all lessons
  - Users can request their certificate at any time
- **Daily Lesson Automation:**
  - Automated daily lesson delivery using a scheduled webhook (cron-job.org)
  - Each user receives the next lesson every day

## Pending Areas for Improvement
- **Subscription Integration:**
  - Add payment support (e.g., M-Pesa via Paystack/Flutterwave) for premium content or features
- **Admin Tools:**
  - Create a web admin page or WhatsApp admin mode for adding/editing lessons without code changes
- **Advanced Certificate Delivery:**
  - Allow users to download or receive certificates as files or via email
- **Database Integration:**
  - Use a real database for more reliable, scalable storage (especially on cloud platforms)
- **User Experience Enhancements:**
  - Add reminders, more conversational features, or personalized learning paths

## Getting Started

### Prerequisites
- Python 3.8+
- A Twilio account (for WhatsApp API access)
- A Render account (for cloud deployment)

### Setup Instructions
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_NUMBER`
   - `DAILY_LESSON_SECRET`
4. **Run the Flask app:**
   ```bash
   python app.py
   ```

### Daily Automation
- Use a free scheduler (like cron-job.org) to trigger the `/send-daily-lessons` endpoint for daily lesson delivery.

---

Feel free to reach out for help or clarification at any step! 