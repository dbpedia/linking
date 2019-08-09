from OntoSimImports import *
import OntoSimConstants as cnst

vec_dim = 300

def assignVar():
  
  conf_1 = {
      'dict_fl_nm': 'ontodata/dict/dict_fast.json',
      'ip_fl_nm': 'ontodata/modifylbl/source.json',
      'op_fl_nm': 'ontodata/fastentity/source_fast'
  }

  conf_2 = {
      'dict_fl_nm': 'ontodata/dict/dict_fast.json',
      'ip_fl_nm': 'ontodata/modifylbl/target.json',
      'op_fl_nm': 'ontodata/fastentity/target_fast'
  }  
  
  conf_arr = []
  conf_arr.append(conf_1)
  conf_arr.append(conf_2)  
  
  return conf_arr


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


def getFastTxtVecSimple(conf, data, entity_dict_vec):
  
  for key in data:
    words = data[key]['altLbl'].split()
    embed_vec = np.asarray([0.0] * vec_dim) #eg 300d for fastText
    for word in words:
      embed_vec = np.add(embed_vec, np.asarray(entity_dict_vec[word]))

    data[key]['vector'] = embed_vec.tolist()
      
  return data


def getFastTxtVecMean(conf, data, entity_dict_vec):
  
  for key in data:
    words = data[key]['altLbl'].split()
    embed_vec = np.asarray([0.0] * vec_dim) #eg 300d for fastText
    for word in words:
      embed_vec = np.add(embed_vec, np.asarray(entity_dict_vec[word]))

    embed_vec /= len(words)
    data[key]['vector'] = embed_vec.tolist()
      
  return data


def saveFile(fast_dict, conf, ext):
  with open(cnst.code_path+conf['op_fl_nm']+ext, 'w') as outfile:
    json.dump(fast_dict, outfile, indent=4)


#################### MAIN CODE START ####################
def entityToVec():
  try:
    print("#################### EntityToVector START ####################")
    conf_arr = assignVar()

    #   for conf in conf_arr:
    #     entity_dict_vec = loadDictVec(conf)
    #     data = loadFile(conf)
    #     fast_dict = getFastTxtVecSimple(conf, data, entity_dict_vec)
    #     saveFile(fast_dict, conf, "_simple.json")
    #     time.sleep(30) #wait for 30 seconds

    for conf in conf_arr:
      entity_dict_vec = loadDictVec(conf)
      data = loadFile(conf)
      fast_dict = getFastTxtVecMean(conf, data, entity_dict_vec)
      saveFile(fast_dict, conf, "_mean.json")
      time.sleep(cnst.wait_time)

  except Exception as exp:
    raise exp
  finally:
    print("#################### EntityToVector FINISH ####################")


  
#################### MAIN CODE END ####################