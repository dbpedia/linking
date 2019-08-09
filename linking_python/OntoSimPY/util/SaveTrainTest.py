import sys

sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst
from Tree import Tree
from TreeTyp import TreeTyp


def assignVar():
    conf_300 = [
        {
            'fl_nm': 'ontodata/finalentity/300/source_300_mean.json',
            'op_file': "ontodata/train_test_tree/source_300_mean.pt"
        }
    ]

    conf_arr = []
    conf_arr.append(conf_300)

    return conf_arr


def loadEmbeddings(conf_file):
    embeddings = {}
    file_nm = cnst.code_path + conf_file['fl_nm']
    with open(file_nm) as f:
        embeddings = json.load(f)

    return embeddings


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


def generateRootTrees(embeddings, fasttext_model):
    trees = OrderedDict()  # remembers the order that keys were first inserted
    for src_embed_key in embeddings:
        if (embeddings[src_embed_key]['entityTyp'] == 'Class'):
            p_vec = getEmbedVec(src_embed_key, embeddings, fasttext_model)
            root_tree = Tree(src_embed_key, TreeTyp.ROOT[0], p_vec)
            child_node_lst = list()
            embed_obj = embeddings[src_embed_key]

            # for parent subtree
            tmp_obj = embed_obj["parentCls"]
            if (tmp_obj and tmp_obj[0].strip() != "http://www.w3.org/2002/07/owl#Thing"):  # if parent exist
                tmp_tree = getgenerateTree(TreeTyp.PARENT, embed_obj["parentCls"], embeddings, fasttext_model)
                child_node_lst = child_node_lst + copy.deepcopy(tmp_tree)

            # for child subtree
            tmp_obj = embed_obj["childCls"]
            if (tmp_obj and tmp_obj[0].strip() != "http://www.w3.org/2002/07/owl#Nothing"):  # if child exist
                tmp_tree = getgenerateTree(TreeTyp.CHILD, embed_obj["childCls"], embeddings, fasttext_model)
                child_node_lst = child_node_lst + copy.deepcopy(tmp_tree)

            # for equivalent subtree
            tmp_obj = embed_obj["eqCls"]
            if (tmp_obj):  # if equivalent class exist
                tmp_tree = getgenerateTree(TreeTyp.EQCLS, embed_obj["eqCls"], embeddings, fasttext_model)
                child_node_lst = child_node_lst + copy.deepcopy(tmp_tree)

            # for disjoint subtree
            tmp_obj = embed_obj["disjointCls"]
            if (tmp_obj):  # if equivalent class exist
                tmp_tree = getgenerateTree(TreeTyp.DISJCLS, embed_obj["disjointCls"], embeddings, fasttext_model)
                child_node_lst = child_node_lst + copy.deepcopy(tmp_tree)

            # for restriction subtree
            tmp_obj = embed_obj["restriction"]
            if (tmp_obj):
                tmp_tree = getgenerateTree(TreeTyp.RES, embed_obj["restriction"], embeddings, fasttext_model)
                child_node_lst = child_node_lst + copy.deepcopy(tmp_tree)

            root_tree.children = child_node_lst
            trees[src_embed_key] = root_tree

    return trees


def saveDataset(embeddings, conf):
    torch.save(embeddings, cnst.code_path + conf['op_file'])


#################### Main Code START ####################
def saveTrainTest():
    try:
        print("#################### SaveTrainTest START ####################")

        print('fastText model Loads START:- ' + str(datetime.datetime.now()))
        fasttext_model = load_model(cnst.faxt_text_model_path + "wiki.en.bin")
        print('fastText model Loads END:- ' + str(datetime.datetime.now()))

        conf_arr = assignVar()

        for conf in conf_arr:
            for conf_file in conf:
                embeddings = loadEmbeddings(conf_file)
                trees = generateRootTrees(embeddings, fasttext_model)
                saveDataset(trees, conf_file)
                time.sleep(cnst.wait_time)
    except Exception as exp:
        raise exp
    finally:
        print("#################### SaveTrainTest FINISH ####################")

#################### Main Code END ####################


if __name__ == "__main__":
    saveTrainTest()