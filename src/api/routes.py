from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Dummy data structures for demonstration purposes
native_speakers = [
    {"id": 1, "language": "English", "availability": True},
    {"id": 2, "language": "Spanish", "availability": True},
]

sessions = []

def match_native_speaker(user_language):
    for speaker in native_speakers:
        if speaker["language"] == user_language and speaker["availability"]:
            return speaker
    return None

def send_confirmation_email(user_email, session_id):
    sender_email = "noreply@axentx.com"
    receiver_email = user_email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your Live Conversation Session Confirmation"

    body = f"Your session {session_id} has ended. Thank you for using our service!"
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, "yourpassword")
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

@app.route('/sessions', methods=['POST'])
def create_session():
    user_data = request.json
    user_language = user_data.get('language')
    user_email = user_data.get('email')

    matched_speaker = match_native_speaker(user_language)
    if not matched_speaker:
        return jsonify({"error": "No available native speaker found"}), 400

    session_id = str(uuid.uuid4())
    session_start_time = datetime.now()
    session_end_time = session_start_time + timedelta(minutes=15)

    session = {
        "id": session_id,
        "user_language": user_language,
        "speaker_id": matched_speaker["id"],
        "start_time": session_start_time.isoformat(),
        "end_time": session_end_time.isoformat(),
    }

    sessions.append(session)

    # Simulate session end and send confirmation email
    send_confirmation_email(user_email, session_id)

    return jsonify({"session_id": session_id}), 201

if __name__ == '__main__':
    app.run(debug=True)