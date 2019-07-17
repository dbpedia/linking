from flask import make_response, Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import json
from json import dumps
from flask_jsonpify import jsonify
import traceback

from Modify_Label import modifyLblMain

app = Flask(__name__)
# api = Api(app)
CORS(app) # This will enable CORS for all routes

class OntoSimMain(Resource):

    @app.route('/OntoSimPyMain/ontorestservice/ontopy/task2', methods=['POST'])
    def getDict():
        try:
            retVal = request.get_json()
            retVal = modifyLblMain(False, request.get_json())
            retVal = json.dumps(retVal)
        except Exception as e:
            retVal = json.loads('{  "msg" : { "msg_val" : "" } }')
            retVal['msg']['msg_val'] = str(e)
            retVal = json.dumps(retVal)
        return retVal


    @app.route('/OntoSimPyMain/ontorestservice/ontopy/testtask', methods=['GET'])
    def testWebService():
        return "Ontosim : python web service is working!"

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #     return response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
