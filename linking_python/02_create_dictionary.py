import json
import time
import traceback

#load gloabal variables
colab_code_path = "/content/drive/My Drive/deep_learning/OntoSimilarity/"
code_path = colab_code_path
#local_code_path = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/FinalCode/GCP/OntoSimilarity/"
#code_path = local_code_path
#gcp_code_path = "/home/jaydeep_chakraborty_1988/research/OntoSimilarity/"
#code_path = gcp_code_path

def assignVar():
  
  conf = {
      'fl_nm_arr' : ['data/ip_op/source.json', 
                    'data/ip_op/target.json',
                    'data/ip_op/source_ObjProp.json',
                    'data/ip_op/target_ObjProp.json',
                    'data/ip_op/source_Rel.json',
                    'data/ip_op/target_Rel.json'],
      'dict_fl' : 'data/dict/dict.txt'
  }
  
  return conf

def loadFile(conf_fl):
  
  fl_nm = code_path+conf_fl
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

  print('No of Unique Words:- '+str(len(onto_unq_words)))
  return onto_unq_words

def writeDict(conf, entity_dict):
  with open(code_path+conf['dict_fl'], "w") as file:
    for entity in entity_dict:
      file.write(entity+"\n")

#################### MAIN CODE START ####################
try:
  
  conf = assignVar()
  entity_dict = crtDict(conf)
  writeDict(conf, entity_dict)
  
  time.sleep(30) #wait for 30 seconds
  
except Exception:
   print(traceback.format_exc())
finally:
  print("#################### FINISH ####################")
  
#################### MAIN CODE END ####################
