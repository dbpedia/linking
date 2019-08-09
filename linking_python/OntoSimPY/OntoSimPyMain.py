from SaveIntData import saveIntData
from ModifyLabel import modifyLblMain
from CreateDictionary import crtDictMain
from DictionaryToVector import dictToVec
from EntityToVector import entityToVec
from EntityVecModify import modEntityVec
from GenWordSim import genWordSim
from OntoEvaluation import ontoEval
from OntoFinish import ontoFinish
from OntoSimImports import *
import OntoSimConstants as cnst

app = Flask(__name__)
# This will enable CORS for all routes
CORS(app)

class OntoSimPyMain(Resource):

    @app.route('/OntoSimPyMain/ontorestservice/ontopy/task2', methods=['POST'])
    def ontoPyMtdh():
        try:
            retVal = ""
            saveIntData(request.get_json())
            modifyLblMain()
            crtDictMain()
            dictToVec()
            entityToVec()
            modEntityVec()
            genWordSim()
            ontoEval()
            retVal = ontoFinish()

            retVal = json.dumps(retVal)

        except Exception as e:
            print(traceback.format_exc())
            Onto_Json_Fl = "ontosim.json"
            with open(Onto_Json_Fl) as json_file:
                retVal = json.load(json_file)

            retVal['msg']['msg_val'] = "Error Happened"
            retVal['msg']['msg_cause'] = str(e)
            retVal = json.dumps(retVal)

        return retVal


    @app.route('/OntoSimPyMain/ontorestservice/ontopy/testtask', methods=['GET'])
    def testWebService():
        return "Ontosim : python web service is working!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
