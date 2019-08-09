from OntoSimImports import *
import OntoSimConstants as cnst


def assignVar():
    conf = {
        'fl_nm_arr': ['ontodata/modifylbl/source.json',
                      'ontodata/modifylbl/target.json'],
        'dict_fl': 'ontodata/dict/dict.txt'
    }

    return conf


def loadFile(conf_fl):
    fl_nm = cnst.code_path + conf_fl
    with open(fl_nm) as f:
        data = json.load(f)

    return data


def crtDict(conf):
    onto_unq_words = []
    for conf_fl in conf["fl_nm_arr"]:
        data = loadFile(conf_fl)
        for key in data.keys():
            words = data[key]['altLbl'].split()
            for word in words:
                if word not in onto_unq_words:
                    onto_unq_words.append(word)

    print('No of Unique Words:- ' + str(len(onto_unq_words)))
    return onto_unq_words


def writeDict(conf, entity_dict):
    with open(cnst.code_path + conf['dict_fl'], "w") as file:
        for entity in entity_dict:
            file.write(entity + "\n")


#################### MAIN CODE START ####################
def crtDictMain():
    try:
        print("#################### CreateDictionary START ####################")
        conf = assignVar()
        entity_dict = crtDict(conf)
        writeDict(conf, entity_dict)

        time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### CreateDictionary FINISH ####################")

#################### MAIN CODE END ####################