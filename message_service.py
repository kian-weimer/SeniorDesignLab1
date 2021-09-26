import os
from twilio.rest import Client


def send_text_message(message, number, area_code):
    account_sid = "AC8cf840176ad20a2ec328a6a8513b66c7"
    auth_token = "97131adeee4a101ed9f731e7503731fc"
    
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_='+14158861418',
        to='+1' + area_code + number
    )
