#https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
import message_service
import signal                   
import sys
import time
from LCD import LCD


def button_activated(channel):
    if GPIO.input(16):
        print("do button things")
    # TODO Button Functionality


if __name__ == '__main__':
    
    #should be adjustable on the website
    max_temp = 27
    min_temp = 10
    number = '5635427467'
    
    #sets up pin 16 as an input for an interupt
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(16, GPIO.BOTH, callback=button_activated, bouncetime=50)
    lcd = LCD()
    
    while True:
        start_time = time.time()
        temp = lcd.get_and_print_temp_on()
        if temp > min_temp or temps < max_temp:
            message_service.send_text_message(temp,number)
        
        delay = time.time() - start_time
        if delay < 1:
           time.sleep(1 - delay) # wait for the remaining time in 1s  
        