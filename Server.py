from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from pandas.errors import EmptyDataError
import ast
from flask_cors import CORS
import os
import time

TEMP_FILE = '/home/pi/SeniorDesignLab1/temps.csv'

app = Flask(__name__)
CORS(app)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv(TEMP_FILE)  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

api.add_resource(Users, '/users')  # add endpoints

if __name__ == '__main__':
    print("Waiting for internet connection...")
    response = os.system("ping -c 1 google.com")
    timeout = 0

    #and then check the response...
    while response != 0 and timeout < 600:
        response = os.system("ping -c 1 google.com")
        time.sleep(1)
        timeout = timeout + 1

    time.sleep(2) # there is a small delay after servers are pingable before we can create a server
    
    print("Starting server...")
    app.run('0.0.0.0', 5010)  # run our Flask app
    print("Server started!")
