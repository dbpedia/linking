from OntoSimImports import *
import OntoSimConstants as cnst
from Tree import Tree
from TreeTyp import TreeTyp
from TreeLSTM import TreeLSTM



thing_obj = "http://www.w3.org/2002/07/owl#Thing"
nothing_obj = "http://www.w3.org/2002/07/owl#Nothing"
min_val = -sys.maxsize - 1 #-9223372036854775808
max_val = sys.maxsize #9223372036854775807

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if (torch.cuda.is_available()):
    print("GPU is available ")
    print("Is GPU available :- " + str(torch.cuda.is_available()))
    print("GPU device name :- " + torch.cuda.get_device_name(0))
else:
    print("CPU is available ")

vector_dim = cnst.vec_dim
def assignVar():
    conf = {
        'train_file': "ontodata/finalentity/source_final.json",
        'test_file': "ontodata/finalentity/target_final.json",
        'ws_fl_nm': "ontodata/output/word_sim/",
        'model_file': "model_final_",
        'vector': vector_dim,
        'op_ms_fl_nm': "ontodata/output/word_sim/",
    }

    return conf

def loadData(fl):
    with open(cnst.code_path + fl) as f:
        data = json.load(f)

    return data

def getmodel(conf, data_src_nm):
    model = TreeLSTM(conf["vector"], conf["vector"], device)

    if(data_src_nm == cnst.ds_nm_1):
        model_fl_nm = cnst.onto_model_path + conf["model_file"] + 'anatomy.pt'
    elif(data_src_nm == cnst.ds_nm_2):
        model_fl_nm = cnst.onto_model_path + conf["model_file"] + 'largebio_1.pt'
    elif(data_src_nm == cnst.ds_nm_3):
        model_fl_nm = cnst.onto_model_path + conf["model_file"] + 'largebio_1.pt'
    elif(data_src_nm == cnst.ds_nm_4):
        model_fl_nm = cnst.onto_model_path + conf["model_file"] + 'largebio_1.pt'
    elif(data_src_nm == cnst.ds_nm_5):
        model_fl_nm = cnst.onto_model_path + conf["model_file"] + 'largebio_1.pt'
    elif(data_src_nm == cnst.ds_nm_6):
        model_fl_nm = cnst.onto_model_path + conf["model_file"] + 'largebio_2.pt'
    elif(data_src_nm == cnst.ds_nm_7):
        model_fl_nm = cnst.onto_model_path + conf["model_file"] + 'largebio_2.pt'

    model.load_state_dict(torch.load(model_fl_nm, map_location='cpu'))
    return model

def getEmbedVec(key, embed):
        return embed[key]['vector']

def peek(stack):
    return stack[-1] if stack else None


# SHUNTING YARD ALGORITHM
def populateResultantVec(token_lst, embeddings):
    result = np.array([])
    equations = []
    for token in token_lst:
        if (token == ')'):
            top = peek(equations)
            count = 0
            tmp_result = [0] * vector_dim
            while top[1] is not None and top[1] != '(':
                # if (src_embed_key == 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#CSNK2A1_wt_Allele'):
                #     print("top-1: "+str(top[1]))
                count = count + 1

                if (top[0] == 'owlstr'):
                    tmp_top = top[1].replace("<", "").replace(">", "")
                    tmp_result = np.add(tmp_result, getEmbedVec(tmp_top, embeddings))
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

def populateEntityVec(entity_key, embeddings):
    if ("(" in entity_key):
        expression = entity_key.replace("(", "( ").replace(",", " , ").replace(")", " ) ")
        tokens = expression.split(" ")
        token_lst = []
        for token in tokens:
            if ("" != token and " " != token and "," != token):
                token_lst.append(token)
        result_vec = populateResultantVec(token_lst, embeddings)
    else:
        entity_key = entity_key.replace("<", "").replace(">", "")
        result_vec = getEmbedVec(entity_key, embeddings)

    return result_vec

def getgenerateTree(treetyp, obj_json, embeddings):
    lst = list()
    for obj_key in obj_json:
        obj_vec = populateEntityVec(obj_key, embeddings)
        lst.append(Tree(obj_key, treetyp[0], obj_vec))

    return lst

def generateSrcTrgtTree(trgt_key, src_key, src_embeddings, trgt_embeddings):

    t_vec = getEmbedVec(trgt_key, trgt_embeddings)
    trgt_root_tree = Tree(trgt_key, TreeTyp.ROOT[0], t_vec)
    trgt_embed_obj = trgt_embeddings[trgt_key]
    trgt_child_node_lst = list()

    p_vec = getEmbedVec(src_key, src_embeddings)
    src_root_tree = Tree(src_key, TreeTyp.ROOT[0], p_vec)
    src_embed_obj = src_embeddings[src_key]
    src_child_node_lst = list()

    # if parent of target exist, then only add parent in source
    trgt_tmp_obj = trgt_embed_obj["parentCls"]
    src_tmp_obj = src_embed_obj["parentCls"]
    if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != thing_obj):
        # target parent subtree
        trgt_tmp_tree = getgenerateTree(TreeTyp.PARENT, trgt_embed_obj["parentCls"],trgt_embeddings)
        trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)
    if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != thing_obj
            and src_tmp_obj and src_tmp_obj[0].strip() != thing_obj):
        # source parent subtree
        src_tmp_tree = getgenerateTree(TreeTyp.PARENT, src_embed_obj["parentCls"], src_embeddings)
        src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

    # if child of target exist, then only add child in source
    trgt_tmp_obj = trgt_embed_obj["childCls"]
    src_tmp_obj = src_embed_obj["childCls"]
    if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != nothing_obj):
        # target child subtree
        trgt_tmp_tree = getgenerateTree(TreeTyp.CHILD, trgt_embed_obj["childCls"], trgt_embeddings)
        trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)
    if (trgt_tmp_obj and trgt_tmp_obj[0].strip() != nothing_obj and
            src_tmp_obj and src_tmp_obj[0].strip() != nothing_obj):
        # source child subtree
        src_tmp_tree = getgenerateTree(TreeTyp.CHILD, src_embed_obj["childCls"], src_embeddings)
        src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

    # if equivalent class of target exist, then only add equivalent in source
    trgt_tmp_obj = trgt_embed_obj["eqCls"]
    src_tmp_obj = src_embed_obj["eqCls"]

    if (trgt_tmp_obj and src_tmp_obj):
        # target equivalent subtree
        trgt_tmp_tree = getgenerateTree(TreeTyp.EQCLS, trgt_embed_obj["eqCls"], trgt_embeddings)
        trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)
        # source equivalent subtree
        src_tmp_tree = getgenerateTree(TreeTyp.EQCLS, src_embed_obj["eqCls"], src_embeddings)
        src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

    # if disjoint class of target exist, then only add disjoint in source
    trgt_tmp_obj = trgt_embed_obj["disjointCls"]
    src_tmp_obj = src_embed_obj["disjointCls"]
    if (trgt_tmp_obj and src_tmp_obj):
        # target disjoint subtree
        trgt_tmp_tree = getgenerateTree(TreeTyp.DISJCLS, trgt_embed_obj["disjointCls"], trgt_embeddings)
        trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)
        # source disjoint subtree
        src_tmp_tree = getgenerateTree(TreeTyp.DISJCLS, src_embed_obj["disjointCls"], src_embeddings)
        src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

    # if restriction class of target exist, then only add restriction in source
    trgt_tmp_obj = trgt_embed_obj["restriction"]
    src_tmp_obj = src_embed_obj["restriction"]
    if (trgt_tmp_obj and src_tmp_obj):
        # target restriction subtree
        trgt_tmp_tree = getgenerateTree(TreeTyp.RES, trgt_embed_obj["restriction"], trgt_embeddings)
        trgt_child_node_lst = trgt_child_node_lst + copy.deepcopy(trgt_tmp_tree)
        # source restriction subtree
        src_tmp_tree = getgenerateTree(TreeTyp.RES, src_embed_obj["restriction"], src_embeddings)
        src_child_node_lst = src_child_node_lst + copy.deepcopy(src_tmp_tree)

    trgt_root_tree.children = trgt_child_node_lst
    src_root_tree.children = src_child_node_lst

    return trgt_root_tree, src_root_tree


def ec_cdist(matrix, vector):
    """
    Compute the cosine distances between each row of matrix and vector.
    more the distance less the similarity
    """
    # print(type(matrix))
    # print(matrix.shape) #(3306, 300)
    # print(type(vector))
    # print(vector.shape) #(1, 300)
    sim_dist = scipy.spatial.distance.cdist(matrix, vector, 'euclidean').reshape(-1)
    return sim_dist[0]

def cos_cdist(matrix, vector):
    """
    Compute the cosine distances between each row of matrix and vector.
    cos-dist = 1 - cos(@) // @ is angle between the two vectors
    @ = 0, cost-dist = 1 - 1 = 0
    @ = 90, cost-dist = 1 - 0 = 1
    @ = 180, cost-dist = 1 - (-1) = 2
    @ = 270, cost-dist = 1 - 0 = 1
    @ = 360, cost-dist = 1 - 1 = 0
    more the distance less the similarity
    """
    # print(type(matrix))
    # print(matrix.shape) #(3306, 300)
    # print(type(vector))
    # print(vector.shape) #(1, 300)
    sim_dist = scipy.spatial.distance.cdist(matrix, vector, 'cosine').reshape(-1)
    return sim_dist[0]


def getSimilarityDistUtil(trgt_tree, src_tree, model, dist_ind):
    if(len(trgt_tree.children) == 0 or len(src_tree.children) == 0):
        return min_val #minimum value in python
    else:
        src_pred = model(src_tree, device)
        src_embed_val = src_pred.cpu().detach().numpy()
        src_embed_val = src_embed_val[0]
        src_embed_val = src_embed_val.reshape(1, src_embed_val.shape[0])  # making (300,) to (1,300)

        trgt_pred = model(trgt_tree, device)
        trgt_embed_val = trgt_pred.cpu().detach().numpy()
        trgt_embed_val = trgt_embed_val[0]
        trgt_embed_val = trgt_embed_val.reshape(1, trgt_embed_val.shape[0])  # making (300,) to (1,300)

        # print(type(src_embed_val))
        # print(src_embed_val.shape)
        # print(type(trgt_embed_val))
        # print(trgt_embed_val.shape)
        if(dist_ind == cnst.word_sim_ind_1): #word_sim_ind_1 = "cosine"
            sim_dist = cos_cdist(src_embed_val, trgt_embed_val)
        elif(dist_ind == cnst.word_sim_ind_2): #word_sim_ind_2 = "euclidean"
            sim_dist = ec_cdist(src_embed_val, trgt_embed_val)
        # print(sim_dist)

        return sim_dist

def getSimilarityDist(target_key, src_key, train_data, test_data, model, dist_ind):
    trgt_tree, src_tree = generateSrcTrgtTree(target_key, src_key, train_data, test_data)
    sim_dist = getSimilarityDistUtil(trgt_tree, src_tree, model, dist_ind)
    return sim_dist

def getPredMetaData(word_sim, train_data, test_data, model, dist_ind):

    pred_sim = OrderedDict()
    for target_key in word_sim:
        sources = OrderedDict()
        max_dist = 0
        for src_key in word_sim[target_key]:
            sim_dist = getSimilarityDist(target_key, src_key, train_data, test_data, model, dist_ind)
            sources[src_key] = sim_dist
            if(sim_dist>max_dist):
                max_dist = sim_dist

        for src_key in word_sim[target_key]:
            if(sources[src_key] == min_val):
                sources[src_key] = max_dist

        pred_sim[target_key] = sources

    return pred_sim

def saveOp(op_meta, op_fl_nm):
    with open(cnst.code_path+op_fl_nm, 'w') as outfile:
        json.dump(op_meta, outfile, indent=4)

#################### Main Code START ####################
def ontoPredict(data_src_nm, dist_ind):
    try:
        print("#################### OntoPredict START ####################")
        conf = assignVar()

        model = getmodel(conf, data_src_nm)

        train_data = loadData(conf['train_file'])
        test_data = loadData(conf['test_file'])

        if(dist_ind == cnst.word_sim_ind_1): #word_sim_ind_1 = "cosine"
            word_sim = loadData(conf["ws_fl_nm"] + "word_sim_cosine.json")
        elif(dist_ind == cnst.word_sim_ind_2): #word_sim_ind_2 = "euclidean"
            word_sim = loadData(conf["ws_fl_nm"] + "word_sim_euclidean.json")

        pred_sim = getPredMetaData(word_sim, train_data, test_data, model, dist_ind)

        if(dist_ind == cnst.word_sim_ind_1): #word_sim_ind_1 = "cosine"
            saveOp(pred_sim, conf["op_ms_fl_nm"] + "meta_sim_cosine.json")
        elif(dist_ind == cnst.word_sim_ind_2): #word_sim_ind_2 = "euclidean"
            saveOp(pred_sim, conf["op_ms_fl_nm"] + "meta_sim_euclidean.json")

        time.sleep(cnst.wait_time)
    except Exception as exp:
        raise exp
    finally:
        print("#################### OntoPredict FINISH ####################")

#################### Main Code END ####################
