from SaveIntData import saveIntData
from ModifyLabel import modifyLblMain
from CreateDictionary import crtDictMain
from DictionaryToVector import dictToVec
from EntityToVector import entityToVec
from EntityVecModify import modEntityVec
from GenWordSim import genWordSim
from OntoPredict import ontoPredict
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
            print(sys.version)
            req_json = request.get_json()
            data_param = req_json['db']
            print("Module :- "+str(data_param['db_nm']))

            ###Save the request data in json file(source.json, target.json)
            saveIntData(req_json)

            ###### modify labels of each entity
            modifyLblMain(data_param['db_nm'])

            ###### create dictionary from source and target entities
            crtDictMain()

            #####cnst.frm_vic_1 generate dictionary vectors from model
            #####cnst.frm_vic_2 get dictionary vectors from vector file
            dictToVec(cnst.frm_vic_1)

            #####cnst.frm_vic_1 generate entity vectors from model
            #####cnst.frm_vic_2 get entity vectors from dictionary vector file
            entityToVec(cnst.frm_vic_1, data_param)

            ## Rescaling the data(both train and test)
            ## As we are using LSTM, the output has tobe in range [-1,+1]
            #####cnst.rscl_ind_1 ### -1 ~ +1  (tanh - activation)
            modEntityVec(cnst.rscl_ind_1)

            ## Generating word similarity between target and source
            #####word_sim_ind_1 = "cosine"
            #####word_sim_ind_2 = "euclidean"
            genWordSim(cnst.word_sim_ind_1)

            ## Predict vector for each test data
            #####word_sim_ind_1 = "cosine"
            #####word_sim_ind_2 = "euclidean"
            ontoPredict(cnst.word_sim_ind_1, data_param)

            ## Predict vector for each test data
            #####word_sim_ind_1 = "cosine"
            #####word_sim_ind_2 = "euclidean"
            ontoEval(cnst.word_sim_ind_1, data_param)


            ## it populates the rdf and zip, and delete all the intermediate files
            retVal = ontoFinish()
            retVal = json.dumps(retVal)

        except Exception as e:
            print(traceback.format_exc())
            Onto_Json_Fl = cnst.code_path + "ontosim.json"
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
