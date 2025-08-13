import smtplib
from datetime import datetime, timedelta
from random import randint
from email.message import EmailMessage


def create_verifi_code(lenght: int = 6) -> dict:
    verifi_code = {}
    verifi_code['code'] = ''.join([str(randint(0, 9)) for _ in range(lenght)])
    verifi_code['exp'] = datetime.now() + timedelta(minutes=5)
    return verifi_code


def send_verification_code(
        from_email: str,
        user_email: str,
        server: str,
        port: int,
        pwd: str,
        verifi_code: int) -> str:

    try:

        with smtplib.SMTP(host=server, port=port) as server:

            msg = EmailMessage()
            msg['From'] = from_email
            msg['To'] = user_email
            msg['Subject'] = 'Ваш код подтверждения'
            msg.set_content(f'Ваш код подтверждения: {verifi_code}. Длится 5 минут!')

            server.starttls()
            server.login(from_email, pwd)
            server.send_message(msg)
            return 'sucsess'

    except Exception as e:
        return f'error - {e}'