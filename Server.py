from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
from pandas.errors import EmptyDataError
import ast
from flask_cors import CORS
import os
import time
from LCD import LCD
import sqlite3 as sl
#from mainController import lcd_on

from multiprocessing import Value


TEMP_FILE = '/home/pi/SeniorDesignLab1/temps.csv'
SERVER_FILE = '/home/pi/SeniorDesignLab1/data.db'


def init_database():
    ### THIS SHOULD ONLY BE RAN ONCE
    ### Run this function once to init the database
    ### Reruns will result in lost data

    data = sl.connect(SERVER_FILE)

    vars = {}
    vars["max_temp"] = 31
    vars["min_temp"] = 0
    vars["area_code"] = 112
    vars["phone_number"] = 3456789
    vars["hot_message"] = "The temperature is too hot!"
    vars["cold_message"] = "The temperature is too cold!"
    vars["provider"] = "email.uscc.net"
    vars_df = pd.DataFrame(vars, index=[0])
    vars_df.to_sql('VARS', data)


class Server(Resource):
    # STATIC VAR
    thermometer_plugged_in = None
    LCD_on   = None
    max_temp = None
    min_temp = None
    phone_number = None
    area_code = None

    def get(self):
        try:
            data = pd.read_csv(TEMP_FILE)  # read local CSV
        except EmptyDataError as e:
            time.sleep(0.15)
            try:
                data = pd.read_csv(TEMP_FILE)
            except EmptyDataError as e:
                return {'data': "Error CSV File cannot be read!"}, 500
                
        data = data.to_dict()  # convert dataframe to dict
        data["current_time"] = round(time.time())

        with sl.connect(SERVER_FILE) as sq_data:
            sq_data = sq_data.execute("SELECT * FROM VARS").fetchone()
            data["max_temp"] = sq_data[1]
            data["min_temp"] = sq_data[2]
            data["area_code"] = sq_data[3]
            data["phone_number"] = sq_data[4]
            data["hot_message"] = sq_data[5]
            data["cold_message"] = sq_data[6]
            data["provider"] = sq_data[7]

        if Server.thermometer_plugged_in.value:
            data["thermometer_plugged_in"] = "True"
            return {'data': data}, 200  # return data and 200 OK
        else:
            data["thermometer_plugged_in"] = "False"
            return {'data': data}, 200  # return data and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('LCDStatus', required=False)
        parser.add_argument('max_temp', required=False)
        parser.add_argument('min_temp', required=False)
        parser.add_argument('area_code', required=False)
        parser.add_argument('phone_number', required=False)
        parser.add_argument('hot_message', required=False)
        parser.add_argument('cold_message', required=False)
        parser.add_argument('provider', required=False)
        args = parser.parse_args()  # parse arguments to dictionary

        # call the LCD toggle function here
        if args['LCDStatus']:
            input = args['LCDStatus'].upper()
            if input == "\"ON\"":
                Server.LCD_on.value = True
                LCD.on(True)
                return {'data': {'msg': 'Success, LCD turned ON'}}, 200  # return data with 200 OK
            elif input == "\"OFF\"":
                Server.LCD_on.value = False
                LCD.on(False)
                return {'data': {'msg': 'Success, LCD turned OFF'}}, 200  # return data with 200 OK
            else:
                return {'data': {'msg': "Error 400: LCDStatus " + input + " invalid. Enter \"ON\" or \"OFF\"."}}, 400

        elif args['max_temp'] and args['min_temp']:
            Server.max_temp.value = int(args['max_temp'])
            Server.min_temp.value = int(args['min_temp'])
            with sl.connect(SERVER_FILE) as sq_data:
                sql = '''UPDATE VARS SET max_temp = ''' + str(Server.max_temp.value) + ''';'''
                sq_data.execute(sql)
                sql = '''UPDATE VARS SET min_temp = ''' + str(Server.min_temp.value) + ''';'''
                sq_data.execute(sql)

            return {'data': {'msg': 'Success, Max temp: ' + str(Server.max_temp.value) + " Min temp: " + str(Server.min_temp.value)}}, 200  # return data with 200 OK
            
        elif args['phone_number'] and args['area_code'] and args['provider']:
            Server.phone_number.value = int(args['phone_number'])
            Server.area_code.value = int(args['area_code'])
            with sl.connect(SERVER_FILE) as sq_data:
                sql = '''UPDATE VARS SET phone_number = ''' + str(Server.phone_number.value) + ''';'''
                sq_data.execute(sql)
                sql = '''UPDATE VARS SET area_code = ''' + str(Server.area_code.value) + ''';'''
                sq_data.execute(sql)
                sql = '''UPDATE VARS SET provider = \"''' + args['provider'] + '''\";'''
                sq_data.execute(sql)
            
            return {'data': {'msg': 'Success, New phone number: ' + str(Server.area_code.value) + str(Server.phone_number.value) + " = " + args['area_code'] + args['phone_number']}}, 200  # return data with 200 OK
        elif args['hot_message']:
            with sl.connect(SERVER_FILE) as sq_data:
                sql = '''UPDATE VARS SET hot_message = \"''' + args['hot_message'] + '''\";'''
                sq_data.execute(sql)
        elif args['cold_message']:
            with sl.connect(SERVER_FILE) as sq_data:
                sql = '''UPDATE VARS SET cold_message = \"''' + args['cold_message'] + '''\";'''
                sq_data.execute(sql)
        else:
            return {'data': {'msg': "Error 400: No valid input parameters were passed. No action taken."}}, 400


def main(thermometer_plugged_in, LCD_on, max_temp, min_temp, phone_number, area_code):
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    Server.thermometer_plugged_in = thermometer_plugged_in
    Server.LCD_on = LCD_on
    Server.max_temp = max_temp
    Server.min_temp = min_temp
    Server.phone_number = phone_number
    Server.area_code = area_code

    with sl.connect(SERVER_FILE) as sq_data:
        sq_data = sq_data.execute("SELECT * FROM VARS").fetchone()
        Server.max_temp.value = sq_data[1]
        Server.min_temp.value = sq_data[2]
        Server.area_code.value = sq_data[3]
        Server.phone_number.value = sq_data[4]

    api.add_resource(Server, '/users')  # add endpoints

    print("Waiting for internet connection...")
    response = os.system("ping -c 1 google.com")
    timeout = 0

    # and then check the response...
    while response != 0 and timeout < 600:
        response = os.system("ping -c 1 google.com")
        time.sleep(1)
        timeout = timeout + 1

    time.sleep(2)  # there is a small delay after servers are pingable before we can create a server

    print("Starting server...")

    app.run('0.0.0.0', 5010)  # run our Flask app

if __name__ == '__main__':
    # Calling this file directly will only create the database.
    # To run the server the main() method should be called by another program.
    i = input("Are you sure that you want to generate a new database?\n"
              "\tThis may overwrite the existing database (if it exists).\n"
              "\tEnter 'Y' to confirm... ")
    
    if i == 'Y' or i == 'y':
        init_database()
