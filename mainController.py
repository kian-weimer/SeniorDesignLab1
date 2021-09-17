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

from ctypes import c_char_p


def button_activated(channel):
    if GPIO.input(16):
        print("do button things")
    # TODO Make this turn on the LCD


if __name__ == '__main__':
    
    min_temp = 0
    max_temp = 31
    phone_number = '5635427467'
    alert_sent = False
    
    #sets up pin 16 as an input for an interupt
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(16, GPIO.BOTH, callback=button_activated, bouncetime=50)
    lcd = LCD()

    # Server communication\
    manager = Manager()
    thermometer_plugged_in = manager.Value(c_bool, False)
    LCD_on = manager.Value(c_bool, True)
    server = Process(target=main, args=(thermometer_plugged_in, LCD_on))
    server.start()
    
    while True:
        start_time = time.time()
        temp = lcd.get_and_print_temp_on()
        if type(temp) != int and not temp:
            thermometer_plugged_in.value = False
        else:
            if not thermometer_plugged_in.value:
                thermometer_plugged_in.value = True
            
            if(temp > max_temp and alert_sent == False):
                alert_sent = True
                message_service.send_text_message("too hot", phone_number)
            elif(temp < max_temp):
                alert_sent = False
            
        delay = time.time() - start_time
        if delay < 1:
           time.sleep(1 - delay) # wait for the remaining time in 1s  
        