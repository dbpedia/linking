from OntoSimImports import *
import OntoSimConstants as cnst

# word_sim_ind = "simple"
word_sim_ind = "mean"
# word_sim_ind = "wmd"


def assignVar():

  vec = "_300_"
  ext = ".json"
  fl_path = 'ontodata/finalentity/300/'
  conf = {
          'src_fl_nm': fl_path+'source'+vec+word_sim_ind+ext,
          'trgt_fl_nm': fl_path+'target'+vec+word_sim_ind+ext,
          'op_fl_nm': 'ontodata/output/word_sim/word_sim'+vec+word_sim_ind
        }

  return conf 


def loadDict(conf):
  with open(cnst.code_path+conf['dict_fl_nm']) as f:
    embed_json_data = json.load(f)
    
  return embed_json_data


def loadSrcTrgt(conf):

  with open(cnst.code_path+conf['src_fl_nm']) as f:
    src_data = json.load(f)

  with open(cnst.code_path+conf['trgt_fl_nm']) as f:
    trgt_data = json.load(f)

  return src_data, trgt_data

def populateSrcNpVec(src_data):

  src_vec = []
  source_keys = src_data.keys()
  for src_key in source_keys:
    src_vec.append(src_data[src_key]["vector"])

  src_vec = np.asarray(src_vec)

  return source_keys, src_vec


#The cosine similarity between two vectors is a measure that calculates the cosine of the angle between them.
#cosine of 0° is 1, and it is less than 1 for any angle in the interval (0,π] radians
#The cosine similarity is particularly used in positive space, where the outcome is neatly bounded in [0,1]
#higher cosine ~ more closer ~ it retruns the similairty higher value means higher similarity
def cosine(u, v):
  cosine_sim = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
  if(cosine_sim >= 0.9999999):
    cosine_sim = 1
  return cosine_sim
 
#higher eucledian ~ more closer ~ it returns the similarity between vectors higher value means higher similarity
def eucledian(u, v):
  e_dist = np.sqrt(np.sum((np.array(u)-np.array(v))**2))
  e_sim = 1/(1+e_dist)
    
  return e_sim


def populateWMDVocab(dict_data):
  model_fl = open(faxt_text_model_path+"wmd/WMD.txt", 'w')
  
  dict_len = len(dict_data.keys())
  vec = 300
  model_fl.write(str(dict_len) +" "+str(vec)+"\n")
  for key in dict_data.keys():
    model_fl.write(key +" "+' '.join(str(e) for e in dict_data[key])+"\n")
    
  model_fl.close()
  time.sleep(10) #wait for 10 second


def getWMDModel():
  #WMD, uses the Euclidean distance.
  model = KeyedVectors.load_word2vec_format(faxt_text_model_path+"wmd/WMD.txt")
  return model


def getWordSim(source_data, target_data, model):
  
  final_wmd_sim = {}
  
  for trgt_key in target_data:   #For each target data
    trgt_lbl_arr = target_data[trgt_key]['altLbl'].split()
    tmp_wmd_sim = {}
    
    for src_key in source_data:   #For each source data
      src_lbl_arr = source_data[src_key]['altLbl'].split()
      distance = model.wmdistance(src_lbl_arr, trgt_lbl_arr) #WMD, uses the Euclidean distance.
      sim_val = 1/(1+distance)
      tmp_wmd_sim[src_key] = sim_val

    tmp_wmd_sim_sort = sorted(tmp_wmd_sim.items(), key=operator.itemgetter(1), reverse=True)
    final_wmd_sim[trgt_key] = tmp_wmd_sim_sort
    
  return final_wmd_sim


def wordSim_Simple(source_data, target_data):
  op_copy_cosine = {}
  op_copy_eucledian = {}
  
  for trgt_key in target_data:   #For each target data
    trgt_vec = target_data[trgt_key]["vector"]
    op_key_dist_cosine = {}
    op_key_dist_eucledian = {}
    for src_key in source_data:   #For each source data
      src_vec = source_data[src_key]["vector"]
      op_key_dist_cosine[src_key] = cosine(trgt_vec,src_vec)
      op_key_dist_eucledian[src_key] = eucledian(trgt_vec,src_vec)
      
    sorted_op_key_dist_cosine = sorted(op_key_dist_cosine.items(), key=operator.itemgetter(1), reverse=True)
    sorted_op_key_dist_eucledian = sorted(op_key_dist_eucledian.items(), key=operator.itemgetter(1), reverse=True)
    
    op_copy_cosine[trgt_key] = sorted_op_key_dist_cosine
    op_copy_eucledian[trgt_key] = sorted_op_key_dist_eucledian
    
  return op_copy_cosine, op_copy_eucledian

def cos_cdist(matrix, vector):
  """
  Compute the cosine distances between each row of matrix and vector.
  """
  v = vector.reshape(1, -1)
  return scipy.spatial.distance.cdist(matrix, v, 'cosine').reshape(-1)


def wordSim_Mean(src_np_vec, target_data, source_keys):

  op_copy_cosine = {}

  for trgt_key in target_data:  # For each target data
    op_copy_cosine_tmp = {}
    trgt_vec = target_data[trgt_key]["vector"]
    trgt_vec = np.asarray(trgt_vec)
    result = cos_cdist(src_np_vec, trgt_vec) #matrix, vector
    tmp_inds = np.argpartition(result, cnst.top_k)[:cnst.top_k] #get the indices of the five largest values
    top_inds = tmp_inds[np.argsort(result[tmp_inds])]
    for top_ind in top_inds:
      src_key = list(source_keys)[top_ind]
      cosine_val = result[top_ind]
      op_copy_cosine_tmp[src_key] = 1 - cosine_val

    op_copy_cosine[trgt_key] = op_copy_cosine_tmp

  return op_copy_cosine

def wordSim_WMD(src_data, trgt_data, dict_data):
  populateWMDVocab(dict_data) #populating WMD vocabulary
  model = getWMDModel()
  model.init_sims(replace=True)  # Normalizes the vectors in the word2vec class.
  return getWordSim(src_data, trgt_data, model)


def saveOp(op_meta_cosine, op_fl_nm, ext):
  
  with open(cnst.code_path+op_fl_nm+ext, 'w') as outfile:
    json.dump(op_meta_cosine, outfile, indent=4)


#################### Main Code START ####################
def genWordSim():
  try:
    print("#################### GenWordSim START ####################")
    strt_tm = datetime.datetime.now()
    conf = assignVar()
    print(word_sim_ind)
    if (word_sim_ind == "wmd"):
      dict_data = loadDict(conf)
      src_data, trgt_data = loadSrcTrgt(conf)
      op_sim_cosine = wordSim_WMD(src_data, trgt_data, dict_data)
      saveOp(op_sim_cosine, conf["op_fl_nm"], ".json")
    if (word_sim_ind == "simple"):
      src_data, trgt_data = loadSrcTrgt(conf)
      op_sim_cosine, op_copy_eucledian = wordSim_Simple(src_data, trgt_data)
      saveOp(op_sim_cosine, conf["op_fl_nm"], "_cosine.json")
      saveOp(op_copy_eucledian, conf["op_fl_nm"], "_eucledian.json")
    if (word_sim_ind == "mean"):
      src_data, trgt_data = loadSrcTrgt(conf)
      source_keys, src_np_vec = populateSrcNpVec(src_data)
      print(src_np_vec.shape)
      op_sim_cosine = wordSim_Mean(src_np_vec, trgt_data, source_keys)
      saveOp(op_sim_cosine, conf["op_fl_nm"], "_cosine.json")

      time.sleep(cnst.wait_time)

  except Exception as exp:
    raise exp
  finally:
    end_tm = datetime.datetime.now()
    total_time_taken = end_tm - strt_tm
    print("Total time taken :- " + str(total_time_taken))
    print("#################### GenWordSim FINISH ####################")

#################### Main Code END ####################