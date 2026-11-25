import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


load_dotenv()

mail_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS").lower() == "true",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

async def send_email(
    recipient: str,
    subject: str,
    body: str
):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype=MessageType.html
    )

    mailer = FastMail(mail_config)

    result_msg = ""

    try:
        await mailer.send_message(message)
        result_msg = F"Message sent to {recipient}"
    except Exception as error:
        result_msg = str(error)

    return result_msg