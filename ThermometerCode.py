import time
from w1thermsensor import W1ThermSensor
from w1thermsensor.errors import SensorNotReadyError, NoSensorFoundError, ResetValueError
import os.path

import pandas as pd
from pandas.errors import EmptyDataError

TEMP_FILE = '/home/pi/SeniorDesignLab1/temps.csv'
NULL = -1000

def F2C(degrees):
    if degrees == NULL:
        return NULL
    return (degrees - 32)*5/9


def C2F(degrees):
    if degrees == NULL:
        return NULL
    return degrees*9/5 + 32


def init():
    if os.path.isfile(TEMP_FILE):
        df = pd.read_csv(TEMP_FILE)
        print(df.iloc[-1, 0])
        current_time = round(time.time())
        print(current_time)
        diff = current_time - df.iloc[-1, 0]
        if diff > 300 :
            diff = 300
        for i in range(diff):
            archive_temp(NULL)      


def archive_temp(temp):
    if os.path.isfile(TEMP_FILE):
        finished = False
        tries = 4
        while not finished and tries > 0:
            try:
                df = pd.read_csv(TEMP_FILE)
                pd.read_csv(TEMP_FILE, usecols=['Time(s)', 'Temp(F)', 'Temp(C)'])
                df2 = pd.DataFrame([[round(time.time()), C2F(temp), temp]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])
                df = df.append(df2, ignore_index=True)
                finished = True
            except EmptyDataError as e:
                tries = tries - 1
                time.sleep(0.05)
        if tries == 0:
            df = pd.DataFrame([[round(time.time()), C2F(temp), temp]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])
            for i in range(300):
                df2 = pd.DataFrame([[round(time.time()), NULL, NULL]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])
                df = df.append(df2, ignore_index=True)   
        
    else:
        df = pd.DataFrame([[round(time.time()), C2F(temp), temp]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])
        for i in range(300):
            df2 = pd.DataFrame([[round(time.time()), NULL, NULL]], columns=['Time(s)', 'Temp(F)', 'Temp(C)'], index=['x'])
            df = df.append(df2, ignore_index=True)        

    df_len = len(df.index)
    if df_len > 300:
        df = df.iloc[(df_len - 300):]

    df.to_csv(TEMP_FILE, mode='w', index=False, header=True)


def get_temp():
    try:
        sensor = W1ThermSensor()
        temperature = sensor.get_temperature()
        archive_temp(temperature)
    except (SensorNotReadyError, NoSensorFoundError, ResetValueError) as e:
        print("Caught Error: ", e)
        archive_temp(NULL)
        return False
    return temperature
    

# https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/
