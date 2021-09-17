import time
from w1thermsensor import W1ThermSensor
from w1thermsensor.errors import SensorNotReadyError, NoSensorFoundError

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


def get_temp():
    try:
        sensor = W1ThermSensor()
        temperature = sensor.get_temperature()
        archive_temp(temperature)
    except (SensorNotReadyError, NoSensorFoundError):
        return False
    return temperature
    

# https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
