from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from pandas.errors import EmptyDataError
import ast
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('temps.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

api.add_resource(Users, '/users')  # add endpoints

if __name__ == '__main__':
    app.run('0.0.0.0', 5010)  # run our Flask app