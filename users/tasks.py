from celery import shared_task
import time
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_email(email, code):
    print("Sending...")
    send_mail(
        "Привет новый пользователь",
        f"На держи свой код: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print("Отправлен")

@shared_task
def send_test_email():
    send_mail(
        'Отчет о работе',
        'Привет! Это письмо отправлено через Celery.',
        settings.EMAIL_HOST_USER,
        ['atay@gmail.com'], 
        fail_silently=False,
    )



@shared_task
def say_hello():
    print("Привет! Задача выполнена!")
    time.sleep(5)  
    print("Задача закончена!")