from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_MESSAGING_SERVICE_SID, PHONE_NUMBER
from twilio.rest import Client
import re, requests

from seguridad.models import Shortener

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class Util:
    
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject= data['email_subject'], body=data['template'], to=[data['to_email']], from_email=EMAIL_HOST_USER)
        email.content_subtype ='html'
        email.send()
        
    @staticmethod
    def send_sms(phone, sms):
        client.messages.create(messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID, body=sms, from_=PHONE_NUMBER, to=phone)
        
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        
    @staticmethod
    def get_client_device(request):
        client_device = request.META.get('HTTP_USER_AGENT')
        
        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

        if MOBILE_AGENT_RE.match(client_device):
            return 'mobile'
        else:
            return 'desktop'
        
    @staticmethod
    def get_short_url(request, url):
        try:
            create_short_url = Shortener.objects.create(
                long_url = url
            )
            new_url = request.build_absolute_uri('/short/') + create_short_url.short_url
            return new_url
        except:
            return url