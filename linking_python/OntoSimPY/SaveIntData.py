from OntoSimImports import *
import OntoSimConstants as cnst

def assignVar():
    conf_1 = {
        'src_op_fl_nm': 'ontodata/eclipse/source.json',
        'trgt_op_fl_nm': 'ontodata/eclipse/target.json'
    }

    conf_arr = []
    conf_arr.append(conf_1)

    return conf_arr


def loadSourceTarget(req_data):
    src_val = req_data["src_in_data"]["file"]
    source_data = json.loads(base64.b64decode(src_val).decode('utf-8'))

    trgt_val = req_data["trgt_in_data"]["file"]
    target_data = json.loads(base64.b64decode(trgt_val).decode('utf-8'))

    return source_data, target_data


def saveSrcTrgt(source_data, target_data, conf):
    with open(cnst.code_path + conf['src_op_fl_nm'], 'w') as outfile:
        json.dump(source_data, outfile, indent=4)

    with open(cnst.code_path + conf['trgt_op_fl_nm'], 'w') as outfile:
        json.dump(target_data, outfile, indent=4)


#################### MAIN CODE START ####################
def saveIntData(ipData):
    print("#################### SaveIntData START ####################")
    try:
        conf_arr = assignVar()

        for conf in conf_arr:
            source_data, target_data = loadSourceTarget(ipData)

            saveSrcTrgt(source_data, target_data, conf)

            time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### SaveIntData FINISH ####################")

#################### MAIN CODE END ####################

