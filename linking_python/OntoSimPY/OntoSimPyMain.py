from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import json
from json import dumps
from flask_jsonpify import jsonify

from Modify_Label import modifyLblMain

app = Flask(__name__)

CORS(app)

class OntoSimMain(Resource):
    
    @app.route('/OntoSimPyMain/ontorestservice/ontopy/task2', methods=['POST'])
    def getDict():
        retVal = modifyLblMain(False,request.get_json())
        retVal = json.dumps(retVal)
#        print(type(retVal))
#        print(retVal)
        return retVal


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port='8000')
