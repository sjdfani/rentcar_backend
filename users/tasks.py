from celery import shared_task
from django.core.mail import send_mail
from rentcar_backend.settings import env


@shared_task
def send_email(code: str, to_: str):
    subject = 'Forgot password'
    message = f''' <<< Forgot Password >>>
        Please Enter bellow code in input.
        code: {code}
        If you don't request to change password just ignore this email.
        Good luck.
    '''
    try:
        send_mail(subject, message, env('EMAIL_USER'), [to_])
    except:
        pass
