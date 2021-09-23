#https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
import message_service
import signal                   
import sys
import time
from LCD import LCD

from multiprocessing import Process, Queue, Value, Manager
from ctypes import c_bool, c_char_p

from threading import Thread

from Server import main
lcd = LCD()


def button_activated(channel):
    print("on or off: ", LCD.website_on)
    if GPIO.input(16):
        lcd.on(True)
    elif(not LCD.website_on):
        lcd.on(False)
        

if __name__ == '__main__':
    print("hello")
    #should be adjustable on the website
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
    max_temp = Value('i', True)
    min_temp = Value('i', True)
    max_temp.value = 31
    min_temp.value = 0
    phone_number = Value('i', True)
    area_code = Value('i', True)
    server = Process(target=main, args=(thermometer_plugged_in, LCD_on, max_temp, min_temp, phone_number, area_code))
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
            
            if(temp > max_temp.value and alert_sent == "good"):
                alert_sent = "hot"
                message_service.send_text_message("too hot", str(phone_number.value), str(area_code.value))
            elif(temp < max_temp.value and alert_sent = "hot"):
                alert_sent = "good"
                
            if(temp < min_temp.value and alert_sent == "good"):
                alert_sent = "cold"
                message_service.send_text_message("cold brr", str(phone_number.value), str(area_code.value))
            elif(temp > min_temp.value and alert_sent = "cold"):
                alert_sent = "good"
            
        delay = time.time() - start_time
        if delay < 1:
           time.sleep(1 - delay) # wait for the remaining time in 1s  
        