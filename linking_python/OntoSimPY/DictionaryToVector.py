from OntoSimImports import *
import OntoSimConstants as cnst


def assignVar():
    conf = {
        'dict_fl': 'ontodata/dict/dict.txt',
        'dict_json': 'ontodata/dict/dict_fast.json'
    }

    return conf


def readDict(conf):
    with open(cnst.code_path + conf["dict_fl"], 'r') as f:
        entity_dict = f.readlines()

    return entity_dict


def loadDictVec(entity_dict, fasttext_model):
    fast_dict = {}
    for entity_word in entity_dict:
        entity_word = entity_word.replace("\n", "")
        vec = fasttext_model.get_word_vector(entity_word)
        fast_dict[entity_word] = vec.tolist()

    return fast_dict


def writeDictVec(conf, entity_dict):
    with open(cnst.code_path + conf['dict_json'], 'w') as outfile:
        json.dump(entity_dict, outfile, indent=4)


#################### MAIN CODE START ####################
def dictToVec():
    try:
        print("#################### DictionaryToVector START ####################")
        print('fastText model Loads START:- ' + str(datetime.datetime.now()))
        fasttext_model = load_model(cnst.faxt_text_model_path + "wiki.en.bin")
        print('fastText model Loads END:- ' + str(datetime.datetime.now()))

        conf = assignVar()
        entity_dict = readDict(conf)
        entity_dict_vec = loadDictVec(entity_dict, fasttext_model)
        writeDictVec(conf, entity_dict_vec)

        time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### DictionaryToVector FINISH ####################")

#################### MAIN CODE END ####################
