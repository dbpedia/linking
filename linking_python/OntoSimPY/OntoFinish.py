from OntoSimImports import *
import OntoSimConstants as cnst


def assignVar():

    conf = {
        'response_fl_nm': 'ontosim.json',
        'final_op_fl_nm': 'ontodata/output/output_final.rdf',
        'zip_dir': 'ontodata/',
        'zip_fl_nm': 'ontodata/output/onto_files.zip'
    }

    return conf

def get_json(conf):
    Onto_Json_Fl = cnst.code_path + conf['response_fl_nm']
    with open(Onto_Json_Fl) as json_file:
        jsonObj = json.load(json_file)
    return jsonObj

def load_final_result(conf):
    file = open(cnst.code_path + conf['final_op_fl_nm'], 'rb')
    fl_base64 = base64.b64encode(file.read()).decode('ascii')
    file.close()
    return fl_base64


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []
    extToCheck = ['.txt', '.json', '.rdf', '.pt']
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            if any(ext in filename for ext in extToCheck):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

            # returning all file paths
    return file_paths

def removeFl(conf):
    # path to folder which needs to be zipped
    directory = cnst.code_path + conf['zip_dir']

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)

    # printing the list of all files to be zipped
    print('Following temporary files will be removed:')
    for file_name in file_paths:
        print(file_name)
        os.remove(file_name)

    #     # writing files to a zipfile
    # with ZipFile(cnst.code_path + conf['zip_fl_nm'], 'w') as zip:
    #     # writing each file one by one
    #     for file in file_paths:
    #         zip.write(file)

    return None



def populateResult(req_data, final_op_data_bs64):

    req_data["final_op_data"]["file_nm"] = "output.rdf"
    req_data["final_op_data"]["file_typ"] = "application/rdf+xml"
    req_data["final_op_data"]["file"] = final_op_data_bs64

    return req_data


#################### Main Code START ####################
def ontoFinish():
    try:
        print("#################### OntoFinish START ####################")

        conf = assignVar()
        req_data = get_json(conf)
        final_fl_base64 = load_final_result(conf)
        req_data = populateResult(req_data, final_fl_base64)
        removeFl(conf)

        time.sleep(cnst.wait_time)
        return req_data

    except Exception as exp:
        raise exp
    finally:
        print("#################### OntoFinish FINISH ####################")

#################### Main Code END ####################