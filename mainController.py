#https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
import message_service
import signal                   
import sys
import time
from LCD import LCD
import ThermometerCode

from multiprocessing import Process, Queue, Value, Manager
from ctypes import c_bool, c_char_p

from threading import Thread

from Server import main
import sqlite3 as sl

SERVER_FILE = '/home/pi/SeniorDesignLab1/data.db'

lcd = LCD()
glo = 0
on = False

def button_activated(channel):
    global on
    if not on:
        lcd.on(True)
        on=True
    elif(not LCD.website_on.value):
        lcd.on(False)
        on=False
        
        
if __name__ == '__main__':
    #should be adjustable on the website
    alert_sent = 'good'
    switch_status = False

    #sets up pin 16 as an input for an interupt
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(16, GPIO.BOTH, callback=button_activated, bouncetime=50)
    
    ThermometerCode.init()

    # Server communication\
    thermometer_plugged_in = Value(c_bool, False)
    LCD_on = Value(c_bool, False)
    LCD.website_on = LCD_on
    max_temp = Value('i', 31)
    min_temp = Value('i', 0)
    phone_number = Value('i', 0)
    area_code = Value('i', 0)
    server = Process(target=main, args=(thermometer_plugged_in, LCD_on, max_temp, min_temp, phone_number, area_code))
    server.start()
        
    while True:
        start_time = time.time()
        temp = lcd.get_and_print_temp_on()

        if type(temp) != int and not temp:
            thermometer_plugged_in.value = False
        else:
            if not thermometer_plugged_in.value:
                thermometer_plugged_in.value = True
            
            if phone_number.value != 0:
                if(temp > max_temp.value and alert_sent == "good"):
                    alert_sent = "hot"
                    with sl.connect(SERVER_FILE) as sq_data:
                        sq_data = sq_data.execute("SELECT * FROM VARS").fetchone()
                        hot_message = sq_data[5]
                        provider = sq_data[7]
                    message_service.send_text_message(hot_message, str(phone_number.value), str(area_code.value), provider)
                elif(temp < max_temp.value and alert_sent == "hot"):
                    alert_sent = "good"

                if(temp < min_temp.value and alert_sent == "good"):
                    alert_sent = "cold"
                    with sl.connect(SERVER_FILE) as sq_data:
                        sq_data = sq_data.execute("SELECT * FROM VARS").fetchone()
                        cold_message = sq_data[6]
                        provider = sq_data[7]
                    message_service.send_text_message(cold_message, str(phone_number.value), str(area_code.value), provider)
                elif(temp > min_temp.value and alert_sent == "cold"):
                    alert_sent = "good"
            
        delay = time.time() - start_time
        if delay < 1:
           time.sleep(1 - delay) # wait for the remaining time in 1s
    