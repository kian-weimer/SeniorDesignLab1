import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# setup for pin input/output
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def button_activated(channel):
    print("do button things")
    # TODO Button Functionality


def switch_activated(channel):
    print("do switch things")
    # TODO switch functionality


# 24 is pin currently
# adding events makes interrupts
GPIO.add_event_detect(24, GPIO.RISING, callback=button_activated)
GPIO.add_event_detect(24, GPIO.RISING, callback=switch_activated)

# main loop for raspberry pi
while True:
    try:
        GPIO.wait_for_edge(23, GPIO.FALLING)

    # will end the loop can use the power off button
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO
        break
