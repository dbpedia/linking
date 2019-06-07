import json
import time
import datetime
from fastText import load_model 
import traceback

#load gloabal variables
colab_code_path = "/content/drive/My Drive/deep_learning/OntoSimilarity/"
code_path = colab_code_path
faxt_text_model_path = "/content/drive/My Drive/deep_learning/"
#local_code_path = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/FinalCode/GCP/OntoSimilarity/"
#code_path = local_code_path
#gcp_code_path = "/home/jaydeep_chakraborty_1988/research/OntoSimilarity/"
#code_path = gcp_code_path

def assignVar():
  
  conf = {
      'dict_fl' : 'data/dict/dict.txt',
      'dict_json' : 'data/dict/dict_fast.json'
  }
  
  return conf

def readDict(conf):
  with open(code_path+conf["dict_fl"], 'r') as f:
    entity_dict = f.readlines()
    
  return entity_dict

def loadDictVec(entity_dict, fasttext_model):
  fast_dict = {}
  for entity_word in entity_dict:
    entity_word = entity_word.replace("\n","")
    vec = fasttext_model.get_word_vector(entity_word)
    fast_dict[entity_word] = vec.tolist()

  return fast_dict

def writeDictVec(conf, entity_dict):
  with open(code_path+conf['dict_json'], 'w') as outfile:
    json.dump(entity_dict, outfile, indent=4)

#################### MAIN CODE START ####################
try:
  
  print('fastText model Loads START:- '+str(datetime.datetime.now()))
  fasttext_model = load_model(faxt_text_model_path+"fasttext/wiki.en.bin")
  print('fastText model Loads END:- '+str(datetime.datetime.now()))
  
  conf = assignVar()
  entity_dict = readDict(conf)
  entity_dict_vec = loadDictVec(entity_dict, fasttext_model)
  writeDictVec(conf, entity_dict_vec)
  
  time.sleep(30) #wait for 30 seconds
  
except Exception:
   print(traceback.format_exc())
finally:
  print("#################### FINISH ####################")
  
#################### MAIN CODE END ####################
