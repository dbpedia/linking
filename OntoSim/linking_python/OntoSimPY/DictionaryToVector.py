from OntoSimImports import *
import OntoSimConstants as cnst

#~~~~~~~~~~~~~~ Vector File ~~~~~~~~~~~~~~#
vec_nm = "dict_fast.json" #pre saved json

#~~~~~~~~~~~~~~ Model ~~~~~~~~~~~~~~#
model_nm = "fast.bin" #model file



def assignVar():
    conf = {
        'dict_fl': 'ontodata/dict/dict.txt',
        'dict_json': 'ontodata/dict/dict_fast.json',
        'model': model_nm,
        'vec_fl': vec_nm
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


def loadPreTrainedDictVec(conf):
    fl_nm = cnst.faxt_text_model_path + conf['vec_fl']
    with open(fl_nm) as f:
        data = json.load(f)

    return data

def chkAllKeyPresentInVec(entity_dict_pretrained, entity_dict_current):
    for entity_key in entity_dict_current:
        entity_key = entity_key.replace("\n", "")
        if(entity_key not in entity_dict_pretrained.keys()):
            return False

    return True


def dictToVecFile(ind):
    print("Creating Vector from "+ ind)
    conf = assignVar()
    entity_dict_pretrained = loadPreTrainedDictVec(conf)
    entity_dict_current = readDict(conf)
    if(chkAllKeyPresentInVec(entity_dict_pretrained, entity_dict_current)):
        writeDictVec(conf, entity_dict_pretrained)
    else:
        raise Exception("Sorry, key is missing in pre-trained vector file")



def dictToVecModel(ind):
    conf = assignVar()
    print("Creating Vector from " + ind + " " + conf['model'])
    print('fastText model Loads START:- ' + str(datetime.datetime.now()))
    fasttext_model = load_model(cnst.faxt_text_model_path + conf["model"])
    print("Model Dimension:- " + str(fasttext_model.get_dimension()))
    print('fastText model Loads END:- ' + str(datetime.datetime.now()))

    entity_dict = readDict(conf)
    entity_dict_vec = loadDictVec(entity_dict, fasttext_model)
    writeDictVec(conf, entity_dict_vec)


#################### MAIN CODE START ####################
def dictToVec(ind):
    try:
        print("#################### DictionaryToVector START ####################")
        if(ind == cnst.frm_vic_1):
            dictToVecModel(cnst.frm_vic_1)
        elif(ind == cnst.frm_vic_2):
            dictToVecFile(cnst.frm_vic_2)

        time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### DictionaryToVector FINISH ####################")

#################### MAIN CODE END ####################
