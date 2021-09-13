import time
from w1thermsensor import W1ThermSensor
import pandas as pd
from pandas.errors import EmptyDataError

TEMP_FILE = '/home/pi/SeniorDesignLab1/temps.csv'

def F2C(degrees):
    return (degrees - 32)*5/9


def C2F(degrees):
    return degrees*9/5 + 32

def archive_temp(temp):
    import os.path
    if os.path.isfile(TEMP_FILE):
        try:
            df = pd.read_csv(TEMP_FILE)
            pd.read_csv(TEMP_FILE, usecols=['Time(s)', 'Temp(F)', 'Temp(C)'])
            df2 = pd.DataFrame([[round(time.time()), C2F(temp), temp]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])
            df = df.append(df2, ignore_index=True)
        except EmptyDataError as e:
            df = pd.DataFrame([[round(time.time()), C2F(temp), temp]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])
    else:
        df = pd.DataFrame([[round(time.time()), C2F(temp), temp]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])

    df_len = len(df.index)
    if df_len > 300:
        df = df.iloc[(df_len - 300):]

    df.to_csv(TEMP_FILE, mode='w', index=False, header=True)

sensor = W1ThermSensor()

while True:
    start_time = time.time()
    temperature = sensor.get_temperature()
    archive_temp(temperature)
    delay = time.time() - start_time
    if delay < 1:
        time.sleep(1 - delay) # wait for the remaining time in 1s
    else:
        print(delay)
    

# https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
