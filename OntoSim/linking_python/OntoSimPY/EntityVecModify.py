from OntoSimImports import *
import OntoSimConstants as cnst

def assignVar():
  conf = {
      'ip_fl_nm_arr': ['ontodata/fastentity/source_fast.json',
                        'ontodata/fastentity/target_fast.json'],
      'op_fl_nm_arr': ['ontodata/finalentity/source_final.json',
                        'ontodata/finalentity/target_final.json']
  }

  return conf



def loadData(file_nm):
    fl_nm = cnst.code_path + file_nm
    with open(fl_nm) as f:
        vec_data = json.load(f)

    #list is always ordered but not dictionary
    encoded_entity = []
    encoded_entity_key = []
    for key in vec_data.keys():
        encoded_entity.append(vec_data[key]['vector'])
        encoded_entity_key.append(key)

    encoded_entity = np.asarray(encoded_entity)

    return encoded_entity, encoded_entity_key, vec_data


def rescaleData(encoded_entity, left_range, right_range):
  
  print("rescaling by normalization, range :- "+ str(left_range) +" "+ str(right_range))
  scaler = MinMaxScaler(feature_range=(left_range, right_range))
  scaler.fit(encoded_entity)
  output_array = scaler.transform(encoded_entity)
  
  output_array = np.asarray(output_array)
  
  return output_array


def rescaleDataPos(encoded_entity):

    output_array = encoded_entity - np.nanmin(encoded_entity)

    return output_array


def populateModifyVec(file_nm, encoded_entity, encoded_entity_key, encoded_entity_mp):

    for idx, key in enumerate(encoded_entity_key):
        encoded_entity_mp[key]['vector'] = encoded_entity[idx].tolist()

    ecdc_fl_nm = file_nm
    with open(cnst.code_path+ecdc_fl_nm, 'w') as outfile:
        json.dump(encoded_entity_mp, outfile, indent=4)
      

def modEntityVecUtil(ind, encoded_entity):

    encoded_entity = rescaleData(encoded_entity, -1, 1)
    return encoded_entity

#################### Main Code START ####################
def modEntityVec(ind):
    try:
        print("#################### EntityVecModify START ####################")
        conf = assignVar()

        # 1) load train data for scaling
        encoded_entity_train, encoded_entity_train_key, encoded_entity_train_mp = loadData(conf["ip_fl_nm_arr"][0])
        # 2) load test data for scaling
        encoded_entity_test, encoded_entity_test_key, encoded_entity_test_mp = loadData(conf["ip_fl_nm_arr"][1])

        # 3) concatenate train and test data for scaling //append
        encoded_entity = np.concatenate((encoded_entity_train, encoded_entity_test))

        print("encoded_entity_train shape:- " + str(encoded_entity_train.shape))
        print("encoded_entity_test shape:- " + str(encoded_entity_test.shape))
        print("encoded_entity shape:- " + str(encoded_entity.shape))

        # 4) rescaling the entire data
        output_array = modEntityVecUtil(ind, encoded_entity)

        print("output_array shape:- " + str(output_array.shape))
        print("min:- " + str(np.nanmin(output_array)) + " max:- " + str(np.nanmax(output_array)))

        # 5) spliting the entire data into train and test data
        output_array_split = np.array_split(output_array, [encoded_entity_train.shape[0]])
        encoded_entity_train = output_array_split[0] #train data
        encoded_entity_test = output_array_split[1]  #test data

        print("encoded_entity_train shape:- " + str(encoded_entity_train.shape))
        print("encoded_entity_test shape:- " + str(encoded_entity_test.shape))


        # 6) write reduced vectors in json object(encoded_entity_train_mp, encoded_entity_test_mp)
        populateModifyVec(conf["op_fl_nm_arr"][0], encoded_entity_train,
                          encoded_entity_train_key, encoded_entity_train_mp)
        populateModifyVec(conf["op_fl_nm_arr"][1], encoded_entity_test,
                          encoded_entity_test_key, encoded_entity_test_mp)

        time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### EntityVecModify FINISH ####################")

#################### Main Code END ####################