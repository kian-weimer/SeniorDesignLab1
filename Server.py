from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
from pandas.errors import EmptyDataError
import ast
from flask_cors import CORS
import os
import time
from LCD import LCD
#from mainController import lcd_on

from multiprocessing import Value


TEMP_FILE = '/home/pi/SeniorDesignLab1/temps.csv'

class Server(Resource):
    # STATIC VAR
    thermometer_plugged_in = None
    LCD_on   = None
    max_temp = None
    min_temp = None
    phone_number = None
    area_code = None
        
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('LCDStatus', required=False)
        args = parser.parse_args()  # parse arguments to dictionary
        print(args)
        data = pd.read_csv(TEMP_FILE)  # read local CSV
        data = data.to_dict()  # convert dataframe to dict

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
        args = parser.parse_args()  # parse arguments to dictionary
        print(args)
        print("\n\nHERE\n\n")

        # call the LCD toggle function here
        if args['LCDStatus']:
            input = args['LCDStatus'].upper()
            if input == "\"ON\"":
                Server.LCD_on.value = True
                print("Turn LCD ON here")
                LCD.on(True)
                print("website: ", LCD.website_on)
                return {'data': {'msg': 'Success, LCD turned ON'}}, 200  # return data with 200 OK
            elif input == "\"OFF\"":
                Server.LCD_on.value = False
                print("Turn LCD OFF here")
                LCD.on(False)
                print("website: ", LCD.website_on)
                return {'data': {'msg': 'Success, LCD turned OFF'}}, 200  # return data with 200 OK
            else:
                return {'data': {'msg': "Error 400: LCDStatus " + input + " invalid. Enter \"ON\" or \"OFF\"."}}, 400
            
        elif args['max_temp'] and args['min_temp']:
            Server.max_temp.value = int(args['max_temp'])
            Server.min_temp.value = int(args['max_temp'])
            print("New max temp: ", Server.max_temp.value)
            print("New min temp: ", Server.min_temp.value)
            return {'data': {'msg': 'Success, Max temp: ' + str(Server.max_temp.value) + " Min temp: " + str(Server.min_temp.value)}}, 200  # return data with 200 OK
            
        elif args['phone_number'] and args['area_code']:
            Server.phone_number.value = int(args['phone_number'])
            Server.area_code.value = int(args['area_code'])
            print("New phone number: ", Server.phone_number.value)
            return {'data': {'msg': 'Success, New phone number: ' + str(Server.area_code.value) + str(Server.phone_number.value) + " = " + args['area_code'] + args['phone_number']}}, 200  # return data with 200 OK
            
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
    main(False, False)

