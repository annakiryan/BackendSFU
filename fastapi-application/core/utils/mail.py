import aiosmtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from core.config import settings

load_dotenv()

SMTP_HOST = settings.smtp.host
SMTP_PORT = settings.smtp.port
SMTP_USERNAME = settings.smtp.username
SMTP_PASSWORD = settings.smtp.password
SMTP_SENDER = settings.smtp.sender


async def send_email_to_customer(email: str, subject: str, message: str) -> None:
    msg = EmailMessage()
    msg["From"] = SMTP_SENDER
    msg["To"] = email
    msg["Subject"] = subject
    msg.set_content(message)

    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
    )
