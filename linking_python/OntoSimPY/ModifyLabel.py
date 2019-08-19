from OntoSimImports import *
import OntoSimConstants as cnst


def assignVar():
    conf_1 = {
        'src_ip_fl_nm': 'ontodata/eclipse/source.json',
        'trgt_ip_fl_nm': 'ontodata/eclipse/target.json',
        'src_op_fl_nm': 'ontodata/modifylbl/source.json',
        'trgt_op_fl_nm': 'ontodata/modifylbl/target.json',
        'removed_utl_fl_nm': 'ontodata/util/removed.txt'
    }

    conf_arr = []
    conf_arr.append(conf_1)

    return conf_arr


def loadSourceTarget(conf):
    source_fl_nm = conf['src_ip_fl_nm']
    target_fl_nm = conf['trgt_ip_fl_nm']
    source_fl_nm = cnst.code_path + source_fl_nm
    with open(source_fl_nm) as f:
        source_data = json.load(f)

    target_fl_nm = cnst.code_path + target_fl_nm
    with open(target_fl_nm) as f:
        target_data = json.load(f)

    return source_data, target_data



def crtAltLblUtl(conf, source_data, target_data, data_src_nm):

    if(data_src_nm == cnst.ds_nm_1):
        ds_fl_nm = "ModfLbl{}".format('Anatomy')
    elif(data_src_nm == cnst.ds_nm_2):
        ds_fl_nm = "ModfLbl{}".format('LargeBio')


    module = __import__(ds_fl_nm)

    removed_fl = open(cnst.code_path + conf['removed_utl_fl_nm'], "w")
    source_data = module.crtAltLbl(conf, source_data, removed_fl)
    target_data = module.crtAltLbl(conf, target_data, removed_fl)
    removed_fl.close()

    return source_data, target_data


def saveSrcTrgt(source_data, target_data, conf):
    with open(cnst.code_path + conf['src_op_fl_nm'], 'w') as outfile:
        json.dump(source_data, outfile, indent=4)

    with open(cnst.code_path + conf['trgt_op_fl_nm'], 'w') as outfile:
        json.dump(target_data, outfile, indent=4)


#################### MAIN CODE START ####################
def modifyLblMain(data_src_nm):
    print("#################### ModifyLabel START ####################")
    try:
        conf_arr = assignVar()

        for conf in conf_arr:
            source_data, target_data = loadSourceTarget(conf)

            source_data, target_data = crtAltLblUtl(conf, source_data, target_data, data_src_nm)

            saveSrcTrgt(source_data, target_data, conf)

            time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### ModifyLabel FINISH ####################")

#################### MAIN CODE END ####################
