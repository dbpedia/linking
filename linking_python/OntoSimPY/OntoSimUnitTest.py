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


class OntoSimUnitTest(object):

    def get_json(self):
        Onto_Json_Fl = "ontosim.json"
        with open(Onto_Json_Fl) as json_file:
            jsonObj = json.load(json_file)
        return jsonObj

    def modify_label(self):
        print("modify label Started")
        try:
            modifyLblMain()
        except Exception as e:
            print(traceback.format_exc())

    def crt_dict(self):
        print("create dictionary Started")
        try:
            crtDictMain()
        except Exception as e:
            print(traceback.format_exc())

    def dict_vec(self):
        print("dictionary to vector Started")
        try:
            dictToVec()
        except Exception as e:
            print(traceback.format_exc())

    def entity_vec(self):
        print("entity to vector Started")
        try:
            entityToVec()
        except Exception as e:
            print(traceback.format_exc())

    def modf_entity_vec(self):
        print("modify entity vector Started")
        try:
            modEntityVec()
        except Exception as e:
            print(traceback.format_exc())

    def gen_word_sim(self):
        print("entity to vector Started")
        try:
            genWordSim()
        except Exception as e:
            print(traceback.format_exc())

    def onto_eval(self):
        print("entity train test save Started")
        try:
            ontoEval()
        except Exception as e:
            print(traceback.format_exc())


    def onto_finish(self):
        print("entity train test save Started")
        try:
            ontoFinish()
        except Exception as e:
            print(traceback.format_exc())

if __name__ == '__main__':
    # OntoSimUnitTest().modify_label()
    # OntoSimUnitTest().crt_dict()
    # OntoSimUnitTest().dict_vec()
    # OntoSimUnitTest().entity_vec()
    # OntoSimUnitTest().modf_entity_vec()
    # OntoSimUnitTest().gen_word_sim()
    OntoSimUnitTest().onto_eval()
    # OntoSimUnitTest().onto_finish()
