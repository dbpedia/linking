import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import re
import json
import traceback
import base64


# In[10]:


#load gloabal variables
# colab_code_path = "/content/drive/My Drive/deep_learning/OntoSimilarity/"
colab_code_path = ""
code_path = colab_code_path
#local_code_path = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/FinalCode/GCP/OntoSimilarity/"
#code_path = local_code_path
#gcp_code_path = "/home/jaydeep_chakraborty_1988/research/OntoSimilarity/"
#code_path = gcp_code_path


# In[11]:


def assignVar():
  
  conf_1 = {
      'src_ip_fl_nm' : 'data/eclipse/source.json',
      'trgt_ip_fl_nm' : 'data/eclipse/target.json',
      'src_op_fl_nm' : 'data/ip_op/source.json',
      'trgt_op_fl_nm' : 'data/ip_op/target.json'
  }
  
  
  conf_arr = []
  conf_arr.append(conf_1)
    
  return conf_arr  


# In[12]:


def loadSourceTargetLocal(conf):
    source_fl_nm = conf['src_ip_fl_nm']
    target_fl_nm = conf['trgt_ip_fl_nm']
    
    source_fl_nm = code_path+source_fl_nm
    with open(source_fl_nm) as f:
        source_data = json.load(f)

    target_fl_nm = code_path+target_fl_nm
    with open(target_fl_nm) as f:
        target_data = json.load(f)
        
    return source_data, target_data

def loadSourceTarget(req_data):

    src_val = req_data["src_in_data"]["file"].replace("data:application/json;base64,","")
    source_data = json.loads(base64.b64decode(src_val).decode('utf-8'))
    
    trgt_val = req_data["trgt_in_data"]["file"].replace("data:application/json;base64,","")
    target_data = json.loads(base64.b64decode(trgt_val).decode('utf-8'))
        
    return source_data, target_data


# In[13]:


def modfWord(word):
  word = word.lower()
  wordnet_lemmatizer = WordNetLemmatizer()
  word = wordnet_lemmatizer.lemmatize(word)
  
  return word

def removeStopWords(word):
  stop_word_lst = ["of","the","system","a","all","at","or", "and", "to", "with"]
  if(word.lower() in stop_word_lst):
    return ""
  else:
    return word

def getEntityWords(entity):
  
  return_words = []
  entity_words = entity.replace("'","").replace('_',' ').replace('-',' ').replace('/',' ').replace('(',' ').replace(')',' ').split()
  wordnet_lemmatizer = WordNetLemmatizer()
  for idx,w in enumerate(entity_words):
    word = entity_words[idx]
    word = word.lower()
    word = wordnet_lemmatizer.lemmatize(word)
    word = removeStopWords(word)
    if(word != ""):
      return_words.append(word)
 
  return return_words


def checkIfRomanNumeral(intVal):
  intVal_Tmp = intVal.upper()
  validRomanNumerals = ["M", "D", "C", "L", "X", "V", "I"]
  for letters in intVal_Tmp:
     if letters not in validRomanNumerals:
        return False

  return True


def chkAlphaNumeric(input):
  return bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', input))


def int_to_roman(input):
  intVal_Tmp = input
  intVal_Tmp = intVal_Tmp.upper()
  nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
  sum = 0
  for i in range(len(intVal_Tmp)):
      try:
          value = nums[intVal_Tmp[i]]
          # If the next place holds a larger number, this value is negative
          if (i+1 < len(intVal_Tmp)) and (nums[intVal_Tmp[i+1]] > value):
              sum -= value
          else: sum += value
      except KeyError:
          raise (ValueError, 'input is not a valid Roman numeral: %s' % intVal_Tmp)
  
  return sum


# In[14]:


def crtAltLbl(conf, data):

  err_key = []
  for key in data.keys():
      alt_word = ""

      if(data[key]['lbl'] is not None):
        words = getEntityWords(data[key]['lbl']) #get all the words separated
        for word in words:
              tmp_word = word

              #if the word is numeric
              if(tmp_word.isdigit()):
                num = str(int(tmp_word))
                alt_word = alt_word + " " + num
                continue

              #if the word is alpha-numeric
              if(chkAlphaNumeric(tmp_word)):
                num = "".join(re.findall('\d+',tmp_word))

                if(len(num)>0):
                  num = str(int(num))
                  alt_word = alt_word + " " + num

                abbr = tmp_word.replace(num,"").lower()
                if(abbr == "s"):
                  alt_word = alt_word + " " + modfWord("Sacral")
                elif(abbr == "l"):
                  alt_word = alt_word + " " + modfWord("Lumbar")
                elif(abbr == "t"):
                  alt_word = alt_word + " " + modfWord("Thoracic")
                elif(abbr == "c"):
                  alt_word = alt_word + " " + modfWord("Cervical")
                elif(abbr == "ca"):
                  alt_word = alt_word + " " + modfWord("Cornu") + " " + modfWord("Ammonis")
                else: #CD4,CD8
                  alt_word = alt_word + " " + modfWord(abbr)
                continue

              #if the word is Roman Integer (alpha)
              if(tmp_word.isalpha() and checkIfRomanNumeral(tmp_word)):
                roman_num = str(int_to_roman(tmp_word))
                if(roman_num.isdigit()):
                  alt_word = alt_word + " " + roman_num
                continue

              #if the word is simple Literal alpha)
              if (tmp_word.isalpha() and (len(tmp_word)>=1)):
                alt_word = alt_word + " " + tmp_word
              else:
                print(tmp_word+'\n') #these words are removed while modifying labels

      else:
        print("label is None" + key)
        err_key.append(key)


      alt_word = ' '.join(sorted(set(alt_word.split()))) #to remove repeat words
      data[key]['altLbl'] = alt_word.strip()
    
  for key in err_key:
    data.pop(key, None)

  return data


def crtAltLblUtl(conf, source_data, target_data):
  
  source_data = crtAltLbl(conf, source_data)
  target_data = crtAltLbl(conf, target_data)
    
  return source_data, target_data


# In[15]:


def saveSrcTrgtLocal(source_data, target_data, conf):
  
  with open(code_path+conf['src_op_fl_nm'], 'w') as outfile:
    json.dump(source_data, outfile, indent=4)
    
  with open(code_path+conf['trgt_op_fl_nm'], 'w') as outfile:
    json.dump(target_data, outfile, indent=4)

def saveSrcTrgt(source_data, target_data, conf, req_data):
    
    source_json = json.dumps(source_data)
    req_data["src_op_data"]["file_nm"] = "source.json"
    req_data["src_op_data"]["file_typ"] = "json"
    print(type(base64.b64encode(source_json.encode('utf-8'))))
    req_data["src_op_data"]["file"] = base64.b64encode(source_json.encode('utf-8')).decode('ascii')

    
    target_json = json.dumps(target_data)
    req_data["trgt_op_data"]["file_nm"] = "target_json.json"
    req_data["trgt_op_data"]["file_typ"] = "json"
    req_data["trgt_op_data"]["file"] = base64.b64encode(target_json.encode('utf-8')).decode('ascii')

    
    return req_data


# In[16]:


#################### MAIN CODE START ####################
def modifyLblMain(isLocal,req_data):
    try:  
      conf_arr = assignVar()

      for conf in conf_arr:
          if(isLocal):
              source_data, target_data = loadSourceTargetLocal(conf) #from local file
          else:
              source_data, target_data = loadSourceTarget(req_data) #from web service
                      
          source_data, target_data = crtAltLblUtl(conf, source_data, target_data)

          if(isLocal):
            saveSrcTrgtLocal(source_data, target_data, conf)
          else:
            retVal = saveSrcTrgt(source_data, target_data, conf, req_data)

      return req_data

    except Exception as exp:
        print(traceback.format_exc())
        raise exp
    finally:
        print("#################### FINISH ####################")
  
#################### MAIN CODE END ####################


# In[ ]:


#modifyLblMain(True, null)

