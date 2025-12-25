import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import socket

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def format_submission_email(content: dict) -> str:
    lines = []

    lines.append(f"Project Title: {content['project_details']['title']}")
    lines.append(f"Description: {content['project_details']['description']}")
    lines.append(f"Code File: {content['project_details']['code_file_path']}")
    lines.append(f"Marks: {content['marks']}")
    lines.append(f"Status: {content['status']}")
    lines.append("\nStudents:")

    for member in content.get("members", []):
        lines.append(f"  - {member['student_name']} ({member['student_id']})")

    return "\n".join(lines)


def send_email_message(to_email: str, subject: str, content: dict):
    message = EmailMessage()
    message["From"] = GMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject
    
    body_text = format_submission_email(content)
    message.set_content(body_text)

    try:
        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=30,
            context=None
        ) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(message)

    except (smtplib.SMTPException, socket.timeout) as e:
        raise RuntimeError(f"Email sending failed: {e}")
