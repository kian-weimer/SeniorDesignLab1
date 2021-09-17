from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from pandas.errors import EmptyDataError
import ast
from flask_cors import CORS
import os
import time

from multiprocessing import Value

TEMP_FILE = '/home/pi/SeniorDesignLab1/temps.csv'

class Users(Resource):
    # STATIC VAR
    thermometer_plugged_in = None
    LCD_on = None

    def get(self):
        data = pd.read_csv(TEMP_FILE)  # read local CSV
        data = data.to_dict()  # convert dataframe to dict

        if Users.thermometer_plugged_in.value:
            data["thermometer_plugged_in"] = "True"
            return {'data': data}, 200  # return data and 200 OK
        else:
            data["thermometer_plugged_in"] = "False"
            return {'data': data}, 200  # return data and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('LCDStatus', required=False)
        args = parser.parse_args()  # parse arguments to dictionary
        print(args)
        print("\n\nHERE\n\n")

        # call the LCD toggle function here
        input = args['LCDStatus'].upper()
        if input == "\"ON\"":
            print("Turn LCD ON here")
        elif input == "\"OFF\"":
            print("Turn LCD OFF here")
        else:
            return {'data': {'msg': "Error 400: LCDStatus " + input + " invalid. Enter \"ON\" or \"OFF\"."}}, 400
        return {'data': {'msg': 'Success'}}, 200  # return data with 200 OK


def main(thermometer_plugged_in, LCD_on):
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    Users.thermometer_plugged_in = thermometer_plugged_in
    Users.LCD_on = LCD_on

    api.add_resource(Users, '/users')  # add endpoints

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
