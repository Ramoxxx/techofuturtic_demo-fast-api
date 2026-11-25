import asyncio
import ssl

import aiosmtplib


async def test_connection():
    try:
        smtp = aiosmtplib.SMTP(
            hostname="smtp.mail.ovh.net",
            port=465,
            use_tls=True,
            tls_context=ssl.create_default_context(),
        )

        await smtp.connect()

        print("SMTP connection successful!")

        await smtp.quit()

    except Exception as error:
        print(f"{type(error).__name__}: {error}")


asyncio.run(test_connection())