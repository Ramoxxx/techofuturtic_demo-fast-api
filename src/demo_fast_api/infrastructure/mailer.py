import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


load_dotenv()

class Mailer:
    _config = ConnectionConfig(
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
    _dep = FastMail(_config)

    async def send_email(self,
        recipients: list[str],
        subject: str,
        body: str
    ):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html
        )


        return await self._dep.send_message(message)            