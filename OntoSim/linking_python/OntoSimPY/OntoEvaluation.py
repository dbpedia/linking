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


def ontoEval(data_src_nm, dist_ind):
    try:
        print("#################### OntoEvaluation START ####################")

        conf = assignVar()

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
        if (data_src_nm == cnst.ds_nm_1):
            word_wt = 0.5
            meta_wt = 0.5
            threshold = 0.01

        final_op = []
        for trgt_key in word_sim_info:
            tmp_op = {"entity1": "", "entity2": "", "measure": ""}

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
            tmp_op['entity1'] = trgt_key
            op = pred_sim_sort[0]
            tmp_op['entity2'] = op[0]
            # tmp_op['measure'] = op[1]
            tmp_op['measure'] = 1.0
            final_op.append(tmp_op)

        saveFinalOP(final_op, conf)
        time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### OntoEvaluation FINISH ####################")
