from OntoSimImports import *
import OntoSimConstants as cnst
from Tree import Tree
from TreeTyp import TreeTyp
from TreeLSTM import TreeLSTM

thing_obj = "http://www.w3.org/2002/07/owl#Thing"
nothing_obj = "http://www.w3.org/2002/07/owl#Nothing"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if (torch.cuda.is_available()):
    print("GPU is available ")
    print("Is GPU available :- " + str(torch.cuda.is_available()))
    print("GPU device name :- " + torch.cuda.get_device_name(0))
else:
    print("CPU is available ")


def assignVar():
    conf_300 = {
        'train_file': 'ontodata/finalentity/300/source_300_mean.json',
        'test_file': "ontodata/finalentity/300/target_300_mean.json",
        'model_file': "model/onto_model/model_300_mean_final.pt",
        'ws_fl_nm': "ontodata/output/word_sim/word_sim_300_mean_cosine.json",
        'vector': 300,
        'op_fl': "ontodata/output/output_final.rdf"
    }

    conf_arr = []
    conf_arr.append(conf_300)

    return conf_arr


def loadEmbeddings(conf):
    with open(cnst.code_path + conf['train_file']) as f:
        train_data = json.load(f)

    with open(cnst.code_path + conf['test_file']) as f:
        test_data = json.load(f)

    return train_data, test_data


def loadWordsim(sim_fl):
    with open(cnst.code_path + sim_fl) as f:
        sim_data = json.load(f)
    return sim_data


def getmodel(conf):
    model = TreeLSTM(conf["vector"], conf["vector"], device)
    model.load_state_dict(torch.load(cnst.onto_model_path + conf["model_file"], map_location='cpu'))
    return model


def getEmbedVec(key, embed, fasttext_model):
    if key in embed:
        return embed[key]['vector']
    else:
        vec = fasttext_model.get_sentence_vector(key)  # this is applicable for data property
        return vec.tolist()


def peek(stack):
    return stack[-1] if stack else None


# SHUNTING YARD ALGORITHM
def populateResultantVec(token_lst, embeddings, fasttext_model):
    result = np.array([])
    equations = []
    for token in token_lst:
        if (token == ')'):
            top = peek(equations)
            count = 0
            tmp_result = [0] * 300
            while top[1] is not None and top[1] != '(':
                # if (src_embed_key == 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#CSNK2A1_wt_Allele'):
                #     print("top-1: "+str(top[1]))
                count = count + 1

                if (top[0] == 'owlstr'):
                    tmp_top = top[1].replace("<", "").replace(">", "")
                    tmp_result = np.add(tmp_result, getEmbedVec(tmp_top, embeddings, fasttext_model))
                else:
                    tmp_result = np.add(tmp_result, top[2])

                equations.pop()
                top = peek(equations)
            equations.pop()  # Discard the '('
            tmp_result = (tmp_result / count)
            # if (src_embed_key == 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#CSNK2A1_wt_Allele'):
            #     print('count :- ' + str(count))
            equations.append(("owlvec", '', tmp_result))
        else:
            # if (src_embed_key == 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#CSNK2A1_wt_Allele'):
            #     print(token)
            equations.append(("owlstr", token, None))

    result = tmp_result
    return result


def populateEntityVec(entity_key, embeddings, fasttext_model):
    if ("(" in entity_key):
        expression = entity_key.replace("(", "( ").replace(",", " , ").replace(")", " ) ")
        tokens = expression.split(" ")
        token_lst = []
        for token in tokens:
            if ("" != token and " " != token and "," != token):
                token_lst.append(token)
        result_vec = populateResultantVec(token_lst, embeddings, fasttext_model)
    else:
        entity_key = entity_key.replace("<", "").replace(">", "")
        result_vec = getEmbedVec(entity_key, embeddings, fasttext_model)

    return result_vec


def getgenerateTree(treetyp, obj_json, embeddings, fasttext_model):
    lst = list()
    for obj_key in obj_json:
        obj_vec = populateEntityVec(obj_key, embeddings, fasttext_model)
        lst.append(Tree(obj_key, treetyp[0], obj_vec))

    return lst


def getPredMetaData(trgt_key, pred_key_lst, src_embeddings, trgt_embeddings, fasttext_model):
    trgt_trees = OrderedDict()  # will contain only one target data at a time
    src_trees = OrderedDict()  # will contain all(5) the source data which are nearer to the target data

    # Creating source trees based on target tree
    for src_embed_key in pred_key_lst:
        p_vec = getEmbedVec(src_embed_key, src_embeddings, fasttext_model)
        src_root_tree = Tree(src_embed_key, TreeTyp.ROOT[0], p_vec)
        src_embed_obj = src_embeddings[src_embed_key]
        src_child_node_lst = list()

        t_vec = getEmbedVec(trgt_key, trgt_embeddings, fasttext_model)
        trgt_root_tree = Tree(trgt_key, TreeTyp.ROOT[0], t_vec)
        trgt_embed_obj = trgt_embeddings[trgt_key]
        trgt_child_node_lst = list()

        # if parent of target exist, then only add parent in source
        trgt_tmp_obj = trgt_embed_obj["parentCls"]
        src_tmp_obj = src_embed_obj["parentCls"]

        if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != thing_obj):  # target subtree
            trgt_tmp_tree = getgenerateTree(TreeTyp.PARENT, trgt_embed_obj["parentCls"], trgt_embeddings,
                                            fasttext_model)
            trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)

        if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != thing_obj and src_tmp_obj and src_tmp_obj[
            0].strip() != thing_obj):
            # source subtree
            src_tmp_tree = getgenerateTree(TreeTyp.PARENT, src_embed_obj["parentCls"], src_embeddings, fasttext_model)
            src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

        # if child of target exist, then only add child in source
        trgt_tmp_obj = trgt_embed_obj["childCls"]
        src_tmp_obj = src_embed_obj["childCls"]

        if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != nothing_obj):  # target subtree
            trgt_tmp_tree = getgenerateTree(TreeTyp.CHILD, trgt_embed_obj["childCls"], trgt_embeddings, fasttext_model)
            trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)

        if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != nothing_obj and src_tmp_obj and src_tmp_obj[
            0].strip() != nothing_obj):
            # source subtree
            src_tmp_tree = getgenerateTree(TreeTyp.CHILD, src_embed_obj["childCls"], src_embeddings, fasttext_model)
            src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

            # if equivalent class of target exist, then only add equivalent in source
        trgt_tmp_obj = trgt_embed_obj["eqCls"]
        src_tmp_obj = src_embed_obj["eqCls"]
        if (trgt_tmp_obj):  # target subtree
            trgt_tmp_tree = getgenerateTree(TreeTyp.EQCLS, trgt_embed_obj["eqCls"], trgt_embeddings, fasttext_model)
            trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)

        if (trgt_tmp_obj and src_tmp_obj):
            # source subtree
            src_tmp_tree = getgenerateTree(TreeTyp.EQCLS, src_embed_obj["eqCls"], src_embeddings, fasttext_model)
            src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

        # if disjoint class of target exist, then only add disjoint in source
        trgt_tmp_obj = trgt_embed_obj["disjointCls"]
        src_tmp_obj = src_embed_obj["disjointCls"]

        if (trgt_tmp_obj):  # target subtree
            trgt_tmp_tree = getgenerateTree(TreeTyp.DISJCLS, trgt_embed_obj["disjointCls"], trgt_embeddings,
                                            fasttext_model)
            trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)

        if (trgt_tmp_obj and src_tmp_obj):
            # source subtree
            src_tmp_tree = getgenerateTree(TreeTyp.DISJCLS, src_embed_obj["disjointCls"], src_embeddings,
                                           fasttext_model)
            src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

        # if disjoint class of target exist, then only add disjoint in source
        trgt_tmp_obj = trgt_embed_obj["restriction"]
        src_tmp_obj = src_embed_obj["restriction"]

        if (trgt_tmp_obj):  # target subtree
            trgt_tmp_tree = getgenerateTree(TreeTyp.RES, trgt_embed_obj["restriction"], trgt_embeddings, fasttext_model)
            trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)

        if (trgt_tmp_obj and src_tmp_obj):
            # source subtree
            src_tmp_tree = getgenerateTree(TreeTyp.RES, src_embed_obj["restriction"], src_embeddings, fasttext_model)
            src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

        trgt_root_tree.children = trgt_child_node_lst
        trgt_trees[src_embed_key] = trgt_root_tree

        src_root_tree.children = src_child_node_lst
        src_trees[src_embed_key] = src_root_tree

    return trgt_trees, src_trees


# The cosine similarity between two vectors is a measure that calculates the cosine of the angle between them.
# cosine of 0° is 1, and it is less than 1 for any angle in the interval (0,π] radians
# The cosine similarity is particularly used in positive space, where the outcome is neatly bounded in [0,1]
# higher cosine ~ more closer ~ it retruns the similairty higher value means higher similarity
def cosine(u, v):
    #   if(np.linalg.norm(u) == 0):
    #     print(trgt_key + "cosine - u - 0")
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def getMetaSim(trgt_trees, src_trees, model):
    meta_sim = []
    lowest_sim_val = sys.float_info.max

    for src_key in src_trees:
        src_tree = src_trees[src_key]
        trgt_tree = trgt_trees[src_key]
        if (src_tree.children and trgt_tree.children):
            src_pred = model(src_tree, device)
            src_embed_val = src_pred.cpu().detach().numpy()
            src_embed_val = src_embed_val[0].tolist()

            trgt_pred = model(trgt_tree, device)
            trgt_embed_val = trgt_pred.cpu().detach().numpy()
            trgt_embed_val = trgt_embed_val[0].tolist()

            cos_sim = cosine(src_embed_val, trgt_embed_val)

            if (cos_sim <= lowest_sim_val):
                lowest_sim_val = cos_sim

        else:
            ##If source or target is blank then cosine sim is zero
            cos_sim = 0

        meta_sim.append([src_key, cos_sim])

    for idx, meta_sim_val in enumerate(meta_sim):
        # If any cosine similarity is zero then replace it with lowest similarity values
        if (meta_sim_val[1] == 0):
            meta_sim[idx] = [meta_sim_val[0], lowest_sim_val]

    return meta_sim


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

    for idx, meta_sim_val in enumerate(meta_sim_arr):
        meta_sim_lst_arr = meta_sim_lst_modf[idx]
        meta_sim_lst_modf[idx] = [meta_sim_lst_arr[0], float(meta_sim_val) / k]

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
    onto1 = SubElement(alignment, 'onto1')
    onto1.text = 'http://bioontology.org/projects/ontologies/fma/fmaOwlDlComponent_2_0'
    onto2 = SubElement(alignment, 'onto2')
    onto2.text = 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl'
    uri1 = SubElement(alignment, 'uri1')
    uri1.text = 'http://bioontology.org/projects/ontologies/fma/fmaOwlDlComponent_2_0'
    uri2 = SubElement(alignment, 'uri2')
    uri2.text = 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl'

    for op in final_op:
        map = SubElement(alignment, 'map')
        cell = SubElement(map, 'Cell')
        entity1 = SubElement(cell, 'entity1')
        entity1.set('rdf:resource', op['entity1'])
        entity2 = SubElement(cell, 'entity2')
        entity2.set('rdf:resource', op['entity2'])
        measure = SubElement(cell, 'measure')
        measure.set('rdf:datatype', 'http://www.w3.org/2001/XMLSchema#float')
        measure.text = str(op['measure'])
        relation = SubElement(cell, 'relation')
        relation.text = '='


    with open(cnst.code_path + conf["op_fl"], "w") as f:
        f.write(prettify(root))


#################### Main Code START ####################
def ontoEval():
    try:
        print("#################### OntoEvaluation START ####################")

        conf_arr = assignVar()

        print('fastText model Loads START:- ' + str(datetime.datetime.now()))
        fasttext_model = load_model(cnst.faxt_text_model_path + "wiki.en.bin")
        print('fastText model Loads END:- ' + str(datetime.datetime.now()))

        for conf in conf_arr:

            model = getmodel(conf)
            train_data, test_data = loadEmbeddings(conf)

            word_sim_info = loadWordsim(conf["ws_fl_nm"])
            final_op = []

            for trgt_key in word_sim_info:
                tmp_op = {"entity1": "", "entity2": "", "measure": ""}
                pred_key_lst = [item for item in word_sim_info[trgt_key]]  # only keys
                trgt_trees, src_trees = getPredMetaData(trgt_key, pred_key_lst, train_data, test_data, fasttext_model)
                meta_sim_lst = getMetaSim(trgt_trees, src_trees, model)
                word_sim_lst = [[key, sim] for key, sim in word_sim_info[trgt_key].items()]
                word_sim_lst_modf, meta_sim_lst_modf = modifyWsMs(word_sim_lst, meta_sim_lst)
                pred_sim_lst = []
                for idx, word_sim in enumerate(word_sim_lst):
                    word_sim_key, word_sim_val = word_sim[0], word_sim[1]
                    if (word_sim_val >= 0.9999999):
                        pred_sim_lst = word_sim_lst
                        break
                    else:
                        new_sim_val = 0.5 * word_sim_lst_modf[idx][1] + 0.5 * meta_sim_lst_modf[idx][1]
                        pred_sim_lst.append([word_sim_key, new_sim_val])

                pred_sim_sort = sorted(pred_sim_lst, key=lambda x: x[1], reverse=True)
                tmp_op['entity1'] = trgt_key
                op = pred_sim_sort[0]
                tmp_op['entity2'] = op[0]
                tmp_op['measure'] = op[1]
                final_op.append(tmp_op)

            saveFinalOP(final_op, conf)
            time.sleep(cnst.wait_time)

    except Exception as exp:
        raise exp
    finally:
        print("#################### OntoEvaluation FINISH ####################")

#################### Main Code END ####################
