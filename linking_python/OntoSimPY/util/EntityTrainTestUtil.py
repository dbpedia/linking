import sys
sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst
from Tree import Tree
from TreeTyp import TreeTyp


################### Debug Code END ####################
trees = torch.load(cnst.code_path + "ontodata/train_test_tree/source_300_mean.pt")
# trees = torch.load(cnst.code_path+"ontodata/train_test_tree/target_300_mean.pt")
print(len(trees))


def crtPrintChildren(tree_obj):
    for children in tree_obj.children:
        print("  " + children.tree_nm + "--(" + children.tree_typ + ")\n")
        print(children.tree_vec)
        print("\n")
        if (len(children.children) > 0):
            crtPrintChildren(children)



#http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#CSNK2A1_wt_Allele
#http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Acute_Myelomonocytic_Leukemia_without_Abnormal_Eosinophils
#http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Stage_I_Adult_Diffuse_Small_Cleaved_Cell_Lymphoma
#tree_row_key = "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Stage_I_Adult_Diffuse_Small_Cleaved_Cell_Lymphoma"

tree_row_key = "http://human.owl#NCI_C33829"


# root_node = Node(tree_row_key)
tree_obj = trees[tree_row_key]
crtPrintChildren(tree_obj)
# print_tree(root_node)

################### Debug Code END ####################
