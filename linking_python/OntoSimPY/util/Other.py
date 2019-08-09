import sys
sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst

conf = {
        'src_fl_nm': 'ontodata/finalentity/300/source_300_mean.json',
        'trgt_fl_nm': "ontodata/finalentity/300/target_300_mean.json"
    }


def loadEmbeddings(conf_file):
    embeddings = {}
    file_nm = cnst.code_path + conf_file['src_fl_nm']
    with open(file_nm) as f:
        embeddings = json.load(f)

    return embeddings


embed = loadEmbeddings(conf)

a = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#CSNK2A1_Gene']['vector']

b = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Gene_Found_In_Organism']['vector']
c = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Human']['vector']

tmp = np.add(b, c) / 2

d = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Gene_Has_Physical_Location']['vector']
e = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#_20_472482-411340']['vector']

tmp = np.add(tmp, (np.add(d, e) / 2))

f = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Gene_In_Chromosomal_Location']['vector']
g = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#_20p13']['vector']

tmp = np.add(tmp, (np.add(f, g) / 2))

i = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Gene_Is_Element_In_Pathway']['vector']
j = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#EGF_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, j) / 2))

k = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#EPO_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, k) / 2))

l = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#IGF-1_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, l) / 2))

m = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#IL2_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, m) / 2))

n = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#IL6_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, n) / 2))

o = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Insulin_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, o) / 2))

p = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#LIS1_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, p) / 2))

q = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Nerve_Growth_Factor_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, q) / 2))

r = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#PDGF_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, r) / 2))

s = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#TPO_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, s) / 2))

t = embed['http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#WNT_Signaling_Pathway']['vector']

tmp = np.add(tmp, (np.add(i, t) / 2))


tmp = np.add(tmp, a) / 15


print(tmp)