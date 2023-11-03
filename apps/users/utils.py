import threading
import phonenumbers

from decouple import config

from eskiz_sms import EskizSMS

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework.exceptions import ValidationError


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data["to_email"]]
        )
        if data.get('content_type') == "html":
            email.content_subtype = 'html'
        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {"code": code}
    )
    Email.send_email({
        "subject": "Registration",
        "to_email": email,
        "body": html_content,
        "content_type": "html"
    })


def send_phone_notification(phone, code):
    email = config('ESKIZ_EMAIL')
    password = config('ESKIZ_PASSWORD')
    message = f"Assalomu alaykum! Sizning tasdiqlash kodingiz: {code}\nIltimos bu tasdiqlash kodini hechkimga bermang!"
    client = EskizSMS(email=email, password=password)
    # client.token.set(your_saved_token)
    client.send_sms(mobile_phone=f"+{phone}", message=message)


def phone_checker(p_number):
    if not (p_number and isinstance(p_number, str) and p_number.isdigit()):
        raise ValidationError("phone_number is not valid")


def phone_parser(p_number, c_code=None):
    try:
        phone_checker(p_number)
        p_number = '+'+p_number
        return phonenumbers.parse(p_number, c_code)
    except Exception as e:
        raise ValidationError("Phone number is not valid")
