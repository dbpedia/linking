from OntoSimImports import *
import OntoSimConstants as cnst


#~~~~~~~~~~~~~~ Vector File ~~~~~~~~~~~~~~#
dict_fl_nm = "dict_fast.json"

#~~~~~~~~~~~~~~ Model ~~~~~~~~~~~~~~#
model_nm = "fast.bin"




def assignVar():

    conf = {
        "model": model_nm,
        "conf_arr": [
            {
                'dict_fl_nm': 'ontodata/dict/dict_fast.json',
                'ip_fl_nm': 'ontodata/modifylbl/source.json',
                'op_fl_nm': 'ontodata/fastentity/source_fast.json'
            },
            {
                'dict_fl_nm': 'ontodata/dict/dict_fast.json',
                'ip_fl_nm': 'ontodata/modifylbl/target.json',
                'op_fl_nm': 'ontodata/fastentity/target_fast.json'
            }
        ]
    }

    return conf


def loadDictVec(conf):
    fl_nm = cnst.code_path + conf['dict_fl_nm']
    with open(fl_nm) as f:
        data = json.load(f)

    return data


def loadFile(conf):
    fl_nm = cnst.code_path+conf['ip_fl_nm']
    with open(fl_nm) as f:
        data = json.load(f)

    return data


def getFastTxtVecSimple(conf, data, entity_dict_vec, db_param):

    for key in data:
        words = data[key]['altLbl'].split()
        embed_vec = np.asarray([0.0] * db_param["vec_dim"]) #eg 300d for fastText
        for word in words:
            embed_vec = np.add(embed_vec, np.asarray(entity_dict_vec[word]))

        data[key]['vector'] = embed_vec.tolist()

    return data


def getFastTxtVecMean(conf, data, entity_dict_vec, db_param):

    for key in data:
        words = data[key]['altLbl'].split()
        embed_vec = np.asarray([0.0] * db_param["vec_dim"]) #eg 300d for fastText
        for word in words:
            embed_vec = np.add(embed_vec, np.asarray(entity_dict_vec[word]))

        embed_vec /= len(words)
        data[key]['vector'] = embed_vec.tolist()

    return data


def getFastTxtVecFast(conf, data, fasttext_model):

    for key in data:
        words = data[key]['altLbl'].replace("\n", "")
        embed_vec = fasttext_model.get_sentence_vector(words);
        data[key]['vector'] = embed_vec.tolist()

    return data


def saveFile(fast_dict, conf):
    with open(cnst.code_path+conf['op_fl_nm'], 'w') as outfile:
        json.dump(fast_dict, outfile, indent=4)


#################### MAIN CODE START ####################
def entityToVec(ind, db_param):
    try:
        print("#################### EntityToVector START ####################")
        conf = assignVar()

        if(ind == cnst.frm_vic_1):
            #####Model of vectors

            print("Creating Vector from " + conf['model'])
            print('fastText model Loads START:- ' + str(datetime.datetime.now()))
            fasttext_model = load_model(cnst.faxt_text_model_path + conf["model"])
            print("Model Dimension:- " + str(fasttext_model.get_dimension()))
            print('fastText model Loads END:- ' + str(datetime.datetime.now()))

            conf_arr = conf["conf_arr"]
            for conf_val in conf_arr:
                data = loadFile(conf_val)
                fast_dict = getFastTxtVecFast(conf_val, data, fasttext_model)
                saveFile(fast_dict, conf_val)
                time.sleep(cnst.wait_time)
        elif(ind == cnst.frm_vic_2):

            # #####Summation of vectors
            #     conf_arr = conf["conf_arr"]
            #     for conf_val in conf_arr:
            #       entity_dict_vec = loadDictVec(conf_val)
            #       data = loadFile(conf_val)
            #       fast_dict = getFastTxtVecSimple(conf_val, data, entity_dict_vec, db_param)
            #       saveFile(fast_dict, conf_val)
            #       time.sleep(cnst.wait_time)

            #####Mean of vectors
            conf_arr = conf["conf_arr"]
            for conf_val in conf_arr:
                entity_dict_vec = loadDictVec(conf_val)
                data = loadFile(conf_val)
                fast_dict = getFastTxtVecMean(conf_val, data, entity_dict_vec, db_param)
                saveFile(fast_dict, conf_val)
                time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### EntityToVector FINISH ####################")



#################### MAIN CODE END ####################
