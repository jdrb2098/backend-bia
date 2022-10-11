from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject= data['email_subject'], body=data['email_body'], to=[data['to_email']], from_email=EMAIL_HOST_USER)
        email.send()