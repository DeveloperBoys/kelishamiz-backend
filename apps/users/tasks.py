from celery import shared_task

from decouple import config
from eskiz_sms import EskizSMS


@shared_task
def send_phone_notification(phone, code):
    email = config('ESKIZ_EMAIL')
    password = config('ESKIZ_PASSWORD')
    message = f"Assalomu alaykum! Sizning tasdiqlash kodingiz: {code}\nIltimos bu tasdiqlash kodini hechkimga bermang!"

    client = EskizSMS(email=email, password=password)
    client.send_sms(mobile_phone=phone, message=message)
