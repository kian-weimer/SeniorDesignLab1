import os
from twilio.rest import Client


def send_text_message(message, number):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_='+14158861418',
        to='+1' + number
    )
