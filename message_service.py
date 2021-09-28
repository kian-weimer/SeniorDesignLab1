import os
from twilio.rest import Client
import sqlite3 as sl
SERVER_FILE = '/home/pi/SeniorDesignLab1/data.db'
import smtplib

def send_text_message(message, number, area_code):
    username = "ryshueh@gmail.com"
    password = ""

    vtext = '1' + area_code + number + "@email.uscc.net"
    message = "woo"
    subject = ""
    msg = ""

    header = 'To:' + number + '\n' + 'From:  ' + username + '\n' + 'Subject: 3rd box message \n'
    print(header)
    mesg = "\n".join([header, message])

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo
    server.login(username,password)
    server.sendmail(username, vtext, mesg)
    server.quit()
    print("i made it thru")
    #)
