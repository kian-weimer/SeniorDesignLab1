#https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
import message_service
import signal                   
import sys
import time
from LCD import LCD

from multiprocessing import Process, Queue, Value, Manager
from ctypes import c_bool
from threading import Thread

from Server import main
lcd = LCD()


def button_activated(channel):
    if GPIO.input(16):
        lcd.on(True)
    elif(not LCD.website_on):
        lcd.on(False)
        

if __name__ == '__main__':
    
    #should be adjustable on the website
    min_temp = 0
    max_temp = 31
    phone_number = ''
    alert_sent = False
    switch_status = False
    
    #sets up pin 16 as an input for an interupt
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(16, GPIO.BOTH, callback=button_activated, bouncetime=50)
    
    #GPIO.setup(13,GPIO.OUT, pull_up_down=GPIO.PUD_UP)

    # Server communication\
    thermometer_plugged_in = Value(c_bool, False)
    LCD_on = Value(c_bool, True)
    server = Process(target=main, args=(thermometer_plugged_in, LCD_on))
    server.start()
    
    while True:
        start_time = time.time()
        temp = lcd.get_and_print_temp_on()
        print("TEMP: ")
        print(temp)

        if type(temp) != int and not temp:
            thermometer_plugged_in.value = False
        else:
            if not thermometer_plugged_in.value:
                thermometer_plugged_in.value = True
            
            if(temp > max_temp and alert_sent == False):
                print("in temp if")
                alert_sent = True
                message_service.send_text_message("too hot", phone_number)
            elif(temp < max_temp):
                alert_sent = False
            
        delay = time.time() - start_time
        if delay < 1:
           time.sleep(1 - delay) # wait for the remaining time in 1s  
        