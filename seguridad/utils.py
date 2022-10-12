from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject= data['email_subject'], body=data['email_body'], to=[data['to_email']], from_email=EMAIL_HOST_USER)
        email.send()
        
    @staticmethod
    def send_sms(phone, msg):
        client.messages.create(body=msg, from_='+12064950580', to=phone)