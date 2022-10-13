from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_MESSAGING_SERVICE_SID
from twilio.rest import Client

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject= data['email_subject'], body=data['template'], to=[data['to_email']], from_email=EMAIL_HOST_USER)
        email.content_subtype ='html'
        email.send()
        
    @staticmethod
    def send_sms(phone, sms):
        client.messages.create(messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID, body=sms, from_='+12064950580', to=phone)