import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    time.sleep(1)

# https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
