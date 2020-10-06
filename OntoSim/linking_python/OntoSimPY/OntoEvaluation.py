from OntoSimImports import *
import OntoSimConstants as cnst

def assignVar():
    conf = {
        'ws_fl_nm': "ontodata/output/word_sim/",
        'op_fl': "ontodata/output/output_final.rdf"
    }

    return conf

def loadData(fl):
    with open(cnst.code_path + fl) as f:
        data = json.load(f)

    return data

def modifyWsMs(word_sim_lst, meta_sim_lst):
    word_sim_lst_modf = copy.deepcopy(word_sim_lst)
    meta_sim_lst_modf = copy.deepcopy(meta_sim_lst)

    word_sim_arr = [item[1] for item in word_sim_lst_modf]  # only similarity values
    meta_sim_arr = [item[1] for item in meta_sim_lst_modf]  # only similarity values

    word_sim_sd = statistics.stdev(word_sim_arr)
    meta_sim_sd = statistics.stdev(meta_sim_arr)

    k = 0.0

    if (word_sim_sd == 0 or meta_sim_sd == 0):
        return word_sim_lst_modf, meta_sim_lst_modf

    k = meta_sim_sd / word_sim_sd

    # print("K: "+str(k))

    if(k>1): # meta-sim is more spread than word-sim, reducing the spread of meta-info
        for idx, _ in enumerate(meta_sim_lst_modf):
            meta_sim_lst_modf[idx][1] = float(meta_sim_lst_modf[idx][1]) / k
    else: # word-sim is more spread than meta-sim, increasing the spread of meta-info
        for idx, _ in enumerate(word_sim_lst_modf):
            word_sim_lst_modf[idx][1] = float(word_sim_lst_modf[idx][1]) * k


    max_word_sim = 0
    max_meta_sim = 0
    for idx, _ in enumerate(meta_sim_lst_modf):
        if(meta_sim_lst_modf[idx][1] > max_meta_sim):
            max_meta_sim = meta_sim_lst_modf[idx][1]
    for idx, _ in enumerate(word_sim_lst_modf):
        if(word_sim_lst_modf[idx][1]>max_word_sim):
            max_word_sim = word_sim_lst_modf[idx][1]

    pow_word_sim = math.floor(math.log(max_word_sim))
    pow_meta_sim = math.floor(math.log(max_meta_sim))
    if(pow_word_sim>pow_meta_sim):
        pow_val = pow_word_sim - pow_meta_sim
        for idx, _ in enumerate(meta_sim_lst_modf):
            meta_sim_lst_modf[idx][1] = float(meta_sim_lst_modf[idx][1]) * pow(10, pow_val)
    else:
        pow_val = pow_meta_sim - pow_word_sim
        for idx, _ in enumerate(word_sim_lst_modf):
            word_sim_lst_modf[idx][1] = float(word_sim_lst_modf[idx][1]) * pow(10, pow_val)

    return word_sim_lst_modf, meta_sim_lst_modf


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def saveFinalOP(final_op, conf):

    root_attr = {'xmlns': 'http://knowledgeweb.semanticweb.org/heterogeneity/alignment', 'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema#'}
    root = Element('rdf:RDF', root_attr)

    alignment = SubElement(root, 'Alignment')

    xml = SubElement(alignment, 'xml')
    xml.text = 'yes'
    level = SubElement(alignment, 'level')
    level.text = '0'
    type = SubElement(alignment, 'type')
    type.text = '??'

    for op in final_op:
        if(op['entity1'] not in cnst.CONSTANT_REMOVE_LST and op['entity2'] not in cnst.CONSTANT_REMOVE_LST):
            map = SubElement(alignment, 'map')
            cell = SubElement(map, 'Cell')
            entity1 = SubElement(cell, 'entity1')
            entity1.set('rdf:resource', op['entity1'])
            entity2 = SubElement(cell, 'entity2')
            entity2.set('rdf:resource', op['entity2'])
            measure = SubElement(cell, 'measure')
            measure.set('rdf:datatype', 'xsd:float')
            measure.text = str(op['measure'])
            relation = SubElement(cell, 'relation')
            relation.text = '='


    with open(cnst.code_path + conf["op_fl"], "w") as f:
        f.write(prettify(root))


#This only for testing purpose
##Testing purpose start
def print_values(trgt_key, word_sim_lst_modf, meta_sim_lst_modf, pred_sim_lst, txt_fl, src_data, trgt_data):
    txt_fl.write("########################################## \n")
    trgt_key_str = trgt_data.get(trgt_key)["lbl"]
    prnt_vl = trgt_key + " (" + trgt_key_str + ")"
    txt_fl.write(prnt_vl + "\n")

    txt_fl.write("Word Similarity \n")
    word_sim_lst_modf_sort = sorted(word_sim_lst_modf, key=lambda x: x[1], reverse=False)
    for word_sim in word_sim_lst_modf_sort:
        word_sim_key, word_sim_val = word_sim[0], word_sim[1]
        word_sim_key_str = src_data.get(word_sim_key)["lbl"]
        prnt_vl = word_sim_key +" ("+word_sim_key_str+") - " +str( word_sim_val)
        txt_fl.write(prnt_vl + "\n")

    txt_fl.write("Meta Similarity \n")
    meta_sim_lst_modf_sort = sorted(meta_sim_lst_modf, key=lambda x: x[1], reverse=False)
    for meta_sim in meta_sim_lst_modf_sort:
        meta_sim_key, meta_sim_val = meta_sim[0], meta_sim[1]
        meta_sim_key_str = src_data.get(meta_sim_key)["lbl"]
        prnt_vl = meta_sim_key + " (" + meta_sim_key_str + ") - " + str(meta_sim_val)
        txt_fl.write(prnt_vl + "\n")

    txt_fl.write("Pred Similarity \n")
    pred_sim_lst_sort = sorted(pred_sim_lst, key=lambda x: x[1], reverse=False)
    for pred_sim in pred_sim_lst_sort:
        pred_sim_key, pred_sim_val = pred_sim[0], pred_sim[1]
        pred_sim_key_str = src_data.get(pred_sim_key)["lbl"]
        prnt_vl = pred_sim_key + " (" + pred_sim_key_str + ") - " + str(pred_sim_val)
        txt_fl.write(prnt_vl + "\n")

    txt_fl.write("########################################## \n")

##Testing purpose end

def ontoEval(dist_ind, db_param):

    try:
        print("#################### OntoEvaluation START ####################")

        conf = assignVar()

        ##Testing purpose start
        # src_data = None
        # trgt_data = None
        # with open(cnst.code_path + 'ontodata/finalentity/source_final.json') as f:
        #     src_data = json.load(f)
        # with open(cnst.code_path + 'ontodata/finalentity/target_final.json') as f:
        #     trgt_data = json.load(f)
        # txt_fl = open("/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/output/pred_op.txt", "a")
        ##Testing purpose stop


        word_sim_info = None
        meta_sim_info = None
        if (dist_ind == cnst.word_sim_ind_1):  # word_sim_ind_1 = "cosine"
            word_sim_info = loadData(conf["ws_fl_nm"] + "word_sim_cosine.json")
            meta_sim_info = loadData(conf["ws_fl_nm"] + "meta_sim_cosine.json")
        elif (dist_ind == cnst.word_sim_ind_2):  # word_sim_ind_2 = "euclidean"
            word_sim_info = loadData(conf["ws_fl_nm"] + "word_sim_euclidean.json")
            meta_sim_info = loadData(conf["ws_fl_nm"] + "meta_sim_euclidean.json")


        word_wt = 0.5
        meta_wt = 0.5
        threshold = 0.0
        if (db_param["db_nm"] == cnst.ds_nm_1):
            word_wt = db_param["word_wt_ds"]
            meta_wt = db_param["meta_wt_ds"]
            threshold = db_param["threshold_ds"]

        final_op = []
        for trgt_key in word_sim_info:

            word_sim_lst = [[key, sim] for key, sim in word_sim_info[trgt_key].items()]
            meta_sim_lst = [[key, sim] for key, sim in meta_sim_info[trgt_key].items()]

            word_sim_lst_modf, meta_sim_lst_modf = modifyWsMs(word_sim_lst, meta_sim_lst)
            pred_sim_lst = []
            for idx, word_sim in enumerate(word_sim_lst_modf):
                word_sim_key, word_sim_val = word_sim[0], word_sim[1]
                if (word_sim_val == 0):
                    pred_sim_lst = word_sim_lst
                    break
                else:
                    for m_key, m_val in meta_sim_lst_modf:
                        if(m_key == word_sim_key):
                            new_sim_val = word_wt * word_sim_val + meta_wt * m_val
                            pred_sim_lst.append([word_sim_key, new_sim_val])

            pred_sim_sort = sorted(pred_sim_lst, key=lambda x: x[1], reverse=False)

            pred_final_op_lst = []
            for val, msr in pred_sim_sort:
                if(msr<threshold and len(pred_final_op_lst)<db_param["op_k"]):
                    pred_final_op_lst.append(val)

            join_str=cnst.join_str_cnst
            if(len(pred_final_op_lst)>0):

                ##Testing purpose start
                # print_values(trgt_key, word_sim_lst_modf, meta_sim_lst_modf, pred_sim_lst, txt_fl, src_data, trgt_data)
                ##Testing purpose stop

                tmp_op = {"entity1": "", "entity2": "", "measure": ""}
                tmp_op['entity1'] = trgt_key
                tmp_op['entity2'] = join_str.join(pred_final_op_lst)
                tmp_op['measure'] = 1.0
                final_op.append(tmp_op)

        saveFinalOP(final_op, conf)
        time.sleep(cnst.wait_time)

        # txt_fl.close()

    except Exception as exp:
        raise exp
    finally:
        print("#################### OntoEvaluation FINISH ####################")
