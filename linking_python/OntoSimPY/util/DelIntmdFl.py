import sys

sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst

def assignVar():

    conf = {
        'zip_dir': 'ontodata/',
        'zip_fl_nm': 'ontodata/output/onto_files.zip'
    }

    return conf

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

#################### Main Code START ####################
def saveTrainTest():
    try:

        conf = assignVar()
        removeFl(conf)

        time.sleep(cnst.wait_time)
    except Exception as exp:
        raise exp
    finally:
        print("#################### DelIntmdFl FINISH ####################")

#################### Main Code END ####################


if __name__ == "__main__":
    saveTrainTest()