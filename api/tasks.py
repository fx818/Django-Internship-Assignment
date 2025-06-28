from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, email, username):
    subject = 'Welcome to the Django!'
    try:
        message = render_to_string('welcome_email.txt', {'username': username})
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
    except Exception as exc:
        raise self.retry(exc=exc) 