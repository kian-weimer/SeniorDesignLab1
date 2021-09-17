import os
from twilio.rest import Client


def send_text_message(message,number):
    print("hello")
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, "97131adeee4a101ed9f731e7503731fc")
    client.messages.create(
        body=message,
        from_='+14158861418',
        to='+1' + number
    )
