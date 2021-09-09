#https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
import RPi.GPIO as GPIO
#import message_service
import signal                   
import sys
import time


def button_activated(channel):
    if GPIO.input(16):
        print("do button things")
    # TODO Button Functionality


if __name__ == '__main__':
    
    #sets up pin 16 as an input for an interupt
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(16, GPIO.BOTH, callback=button_activated, bouncetime=50)
    
    while True:
        try:
            i = 1
        except KeyboardInterrupt:
            GPIO.cleanup()
            break