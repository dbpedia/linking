
##### CODE PATH START (necessary to create the temporary files) #####
#dev_code_path = "/Users/jaydeep/jaydeep_workstation/Workplace/Python/OntoSimilarity_GSOC_local/py_files/OntoSimPY/"
#code_path = dev_code_path

prod_code_path = "usr/ontosim/python/OntoSimPY/"
code_path = prod_code_path

#gcp_code_path = "/home/jchakra1/ontoconn/linking_python/OntoSimPY/"
#code_path = gcp_code_path
##### CODE PATH END #####


##### fast.bin PATH START #####
#dev_faxt_text_model_path = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/OntoConnect/linking/OntoSim/linking_python/py_model/model/fasttext/"
#faxt_text_model_path = dev_faxt_text_model_path

prod_faxt_text_model_path = "usr/ontosim/python/model/fasttext/"
faxt_text_model_path = prod_faxt_text_model_path
##### fast.bin PATH END #####


##### OntoConnect model PATH START #####
#dev_onto_model_path = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/OntoConnect/linking/OntoSim/linking_python/py_model/model/onto_model/"
#onto_model_path = dev_onto_model_path

prod_onto_model_path = "usr/ontosim/python/model/onto_model/"
onto_model_path = prod_onto_model_path

#gcp_onto_model_path = "/home/jchakra1/ontoconn/linking_python/py_model/model/onto_model/"
#onto_model_path = gcp_onto_model_path
##### OntoConnect model PATH START #####

##### DATA-SOURCE START #####
ds_nm_1 = "Anatomy"
ds_nm_2 = "LargeBio-track1"
ds_nm_3 = "LargeBio-track2"
ds_nm_4 = "LargeBio-track3"
ds_nm_5 = "LargeBio-track4"
ds_nm_6 = "LargeBio-track5"
ds_nm_7 = "LargeBio-track6"
##### DATA-SOURCE END #####

frm_vic_1 = "model"
frm_vic_2 = "vec-fl"

rscl_ind_1 = "NEGONE_POSONE" ### -1 ~ +1  (tanh - activation)

word_sim_ind_1 = "cosine"
word_sim_ind_2 = "euclidean"

##### TOP RESULT START #####
top_k = 5
##### TOP RESULT END #####

join_str_cnst="-#-"
wait_time = 15


CONSTANT_REMOVE_LST = ['http://mouse.owl#UNDEFINED_part_of', 'http://human.owl#UNDEFINED_part_of',
                       'http://www.geneontology.org/formats/oboInOwl#Subset', 'http://www.geneontology.org/formats/oboInOwl#SynonymType',
                       'http://www.geneontology.org/formats/oboInOwl#Synonym', 'http://www.geneontology.org/formats/oboInOwl#Definition',
                       'http://www.geneontology.org/formats/oboInOwl#ObsoleteProperty', 'http://www.geneontology.org/formats/oboInOwl#DbXref',
                       'http://mouse.owl#UNDEFINED_is_a', 'http://www.geneontology.org/formats/oboInOwl#ObsoleteClass']
