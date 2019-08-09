from OntoSimImports import *
import OntoSimConstants as cnst
from OntoEncDec import OntoEncDec


epoch_num = cnst.epoch_num
show_epoch_info = cnst.show_epoch_info


def assignVar():
   
  ext = "_mean.json"
#   ext = "_simple.json"
    
  #Modify-1, 300d, [0,1]
  conf_300 = {
      'isReduce': False,
      'ip_fl_nm_arr': ['ontodata/fastentity/source_fast'+ext,
                        'ontodata/fastentity/target_fast'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_300.txt'
  }

  #Modify-1, 256d, [0,1]
  conf_256 = {
      'isReduce': True,
      'vec_len': 256,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/256/source_256'+ext,
                        'ontodata/finalentity/256/target_256'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_256.txt'
  }

  #Modify-1, 224d, [0,1]
  conf_224 = {
      'isReduce': True,
      'vec_len': 224,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/224/source_224'+ext,
                        'ontodata/finalentity/224/target_224'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_224.txt'
  }
  

  #Modify-1, 192d, [0,1]
  conf_192 = {
      'isReduce': True,
      'vec_len': 192,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/192/source_192'+ext,
                        'ontodata/finalentity/192/target_192'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_192.txt'
  }
  
  #Modify-1, 160d, [0,1]
  conf_160 = {
      'isReduce': True,
      'vec_len': 160,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/160/source_160'+ext,
                        'ontodata/finalentity/160/target_160'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_160.txt'
  }


  #Modify-1, 128d, [0,1]
  conf_128 = {
      'isReduce': True,
      'vec_len': 128,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/128/source_128'+ext,
                        'ontodata/finalentity/128/target_128'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_128.txt'
  }
      
      
  #Modify-1, 96d, [0,1]
  conf_96 = {
      'isReduce': True,
      'vec_len': 96,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/96/source_96'+ext,
                        'ontodata/finalentity/96/target_96'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_96.txt'
  }
  
  #Modify-1, 64d, [0,1]
  conf_64 = {
      'isReduce': True,
      'vec_len': 64,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/64/source_64'+ext,
                        'ontodata/finalentity/64/target_64'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_64.txt'
  }
  
  #Modify-1, 32d, [0,1]
  conf_32 = {
      'isReduce': True,
      'vec_len': 32,
      'ip_fl_nm_arr': ['ontodata/finalentity/300/source_300'+ext,
                        'ontodata/finalentity/300/target_300'+ext],
      'op_fl_nm_arr': ['ontodata/finalentity/32/source_32'+ext,
                        'ontodata/finalentity/32/target_32'+ext],
      'loss_fl_nm': 'ontodata/loss/ontomodify/loss_32.txt'
  }
  
 
  conf_arr = []
  conf_arr.append(conf_300)
  # conf_arr.append(conf_256)
#   conf_arr.append(conf_224)
#   conf_arr.append(conf_192)
#   conf_arr.append(conf_160)
#   conf_arr.append(conf_128)
#   conf_arr.append(conf_96)
#   conf_arr.append(conf_64)
#   conf_arr.append(conf_32) 
  
  return conf_arr


def reset_keras(vec):
  from numpy.random import seed
  seed(vec)
  from tensorflow import set_random_seed
  set_random_seed(vec)


def loadTrainingData(conf):
  
  onto_unq_words = []
  encoded_entity = []
  encoded_entity_mp = {}
  
  for file_nm in conf['ip_fl_nm_arr']:
    fl_nm = cnst.code_path+file_nm
    with open(fl_nm) as f:
        vec_data = json.load(f)
  
    for key in vec_data.keys():
      key_word = vec_data[key]['altLbl'].strip()
      if(key_word not in onto_unq_words): #we do not want to add same entity twice (source- bone marrow, target-bone marrow)
        onto_unq_words.append(key_word)
        encoded_entity_mp[key_word] = []
        encoded_entity.append(vec_data[key]['vector'])
  
  encoded_entity = np.asarray(encoded_entity)
  
  return encoded_entity_mp, encoded_entity


class OntoLogger(keras.callbacks.Callback):
  def __init__(self, n):
    self.n = n   # print loss & acc every n epochs

  def on_epoch_end(self, epoch, logs={}):
    epoch_val = (epoch+1)
    if epoch_val % self.n == 0:
      curr_loss = logs.get('loss')
      print("epoch = %4d  loss = %0.10f" % (epoch_val, curr_loss))


# In[23]:


def EncDec_net_Train(conf, encoded_entity, t_callback):
  
  encDec_net_obj = OntoEncDec()
  autoencoder, encoder = encDec_net_obj.main(conf, encoded_entity)
  
  ontoLogger = OntoLogger(show_epoch_info)
  history = autoencoder.fit(encoded_entity, encoded_entity, epochs=epoch_num, verbose=0, batch_size=500, callbacks=[ontoLogger])
  
  output_array = encoder.predict(encoded_entity)

  return output_array, history.history["loss"]


def writeLossFile(conf, loss_list):
  loss_fl_nm = conf['loss_fl_nm']
  with open(cnst.code_path+loss_fl_nm, "w") as f:
    for loss in loss_list:
        f.write(str(loss) + "\n")


def trainEncoderDecoder(conf, encoded_entity):

  output_array, loss_list = EncDec_net_Train(conf, encoded_entity, None)
  writeLossFile(conf, loss_list)
  
  return output_array


def rescaleData(encoded_entity):
  
  print("rescaling by normalization")
  
  scaler = MinMaxScaler(feature_range=(cnst.left_range, cnst.right_range))
  scaler.fit(encoded_entity)
  output_array = scaler.transform(encoded_entity)
  
  output_array = np.asarray(output_array)
  
  return output_array


def populateModifyVec(conf, encoded_entity_mp, output_array):
  
  #First populate output_array values in encoded_entity_mp
  for idx, val in enumerate(encoded_entity_mp.keys()):
    encoded_entity_mp[val] = output_array[idx].tolist() #ndarray are not JSON serializable
  
  
  for idx,file_nm in enumerate(conf['ip_fl_nm_arr']):
    fl_nm = cnst.code_path+file_nm
    with open(fl_nm) as f:
        vec_data = json.load(f)
    
    for key in vec_data.keys():
      key_word = vec_data[key]['altLbl'].strip()
      vec_val = encoded_entity_mp[key_word]
    
      if not vec_val: # this is for debugging pupose
        print(key_word+" is missing - source")
      vec_data[key]['vector'] =  vec_val
      
    ecdc_fl_nm = conf['op_fl_nm_arr'][idx]
    with open(cnst.code_path+ecdc_fl_nm, 'w') as outfile:
        json.dump(vec_data, outfile, indent=4)


# In[28]:


def sendJobStatusEmail(strt_tm, end_tm, total_time_taken):
    email_subj = "Job  Successful"
    fl_nm = "EntityVecModify.py"
    email_body = "Job Start: {}\n"                 "Job End: {}\n"                 "Time taken: {}\n"                 "File Name: {}".format(strt_tm, end_tm, total_time_taken, fl_nm)
    try:
      import send_cust_email
      send_cust_email.sendJobEmail(email_subj, email_body)
    except Exception as exception:
      print("Error: %s!\n\n" % exception)
      email_subj = "Job Exception"
      import send_cust_email
      send_cust_email.sendJobEmail(email_subj, email_body)


#################### Main Code START ####################
def modEntityVec():
    try:
        print("#################### EntityVecModify START ####################")
        strt_tm = datetime.datetime.now()
        conf_arr = assignVar()

        for conf in conf_arr:

            # 1) load training data for auto-encoder
            encoded_entity_mp, encoded_entity = loadTrainingData(conf)

            print("encoded_entity shape:- " + str(encoded_entity.shape))
            print("encoded_entity_mp shape:- " + str(len(encoded_entity_mp)))

            if (conf['isReduce']):
                # # 3) train autoencoder
                reset_keras(conf['vec_len'])
                output_array = trainEncoderDecoder(conf, encoded_entity)
                output_array = rescaleData(output_array)
                print("output_array shape:- " + str(output_array.shape))
            else:
                # # 4) rescale the data
                output_array = rescaleData(encoded_entity)
                print("output_array shape:- " + str(output_array.shape))

            print("min:- " + str(np.nanmin(output_array)) + " max:- " + str(np.nanmax(output_array)))
            # # 5) write rduced vectors in json object
            populateModifyVec(conf, encoded_entity_mp, output_array)

            time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        end_tm = datetime.datetime.now()
        total_time_taken = end_tm - strt_tm
        print("Total time taken :- " + str(total_time_taken))
        # sendJobStatusEmail(strt_tm, end_tm, total_time_taken)
        print("#################### EntityVecModify FINISH ####################")

#################### Main Code END ####################