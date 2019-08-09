import sys
sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst


import matplotlib.pyplot as plt
import tensorflow as tf


def assignVar():
  conf = {
    'src_json': 'ontodata/fastentity/source_fast_mean.json',
    'trgt_json': 'ontodata/fastentity/target_fast_mean.json',
    'entity_vec_hist': 'ontodata/util/entity_vec_hist.png'
  }

  return conf


def getFastVec(conf):
  src_fl_nm = cnst.code_path + conf['src_json']
  with open(src_fl_nm) as f:
    src_entity_dict = json.load(f)


  trgt_fl_nm = cnst.code_path + conf['trgt_json']
  with open(trgt_fl_nm) as f:
    trgt_entity_dict = json.load(f)

  fast_vec_viz = []
  for i in src_entity_dict:
    fast_vec_viz.append(src_entity_dict[i]['vector'])
  for i in trgt_entity_dict:
    fast_vec_viz.append(trgt_entity_dict[i]['vector'])

  return np.asarray(fast_vec_viz)


def plotFastTextDataFrequency(encoded_entity):
    print(encoded_entity.shape)
    print("min:- "+str(np.nanmin(encoded_entity))+" max:- "+str(np.nanmax(encoded_entity)))
    flat_encoded_entity = encoded_entity.flatten()
    print(flat_encoded_entity.shape)

    plt.hist(flat_encoded_entity, bins = [-6,-5,-4,-3,-2,-1,-.9,-.8,-.7,-.6,-.5,
                                          -.4,-.3,-.2,-.1,0,.1,.2,.3,.4,.5,.6,.7,
                                          .8,.9,1,2,3,4,5,6])

    plt.title("Entity FastText vector histogram")
    plt.savefig(os.path.join(cnst.code_path + conf['entity_vec_hist']))


def plotTBEntity(conf):

  src_fl_nm = cnst.code_path + conf['src_json']
  with open(src_fl_nm) as f:
      source_data = json.load(f)

  trgt_fl_nm = cnst.code_path + conf['trgt_json']
  with open(trgt_fl_nm) as f:
      target_data = json.load(f)

  seed = 42
  tf.reset_default_graph()
  tf.set_random_seed(seed)
  np.random.seed(seed)

  embed_onto = []  # for visualization purpose

  metadata_fl_nm = "ontodata/util/metadata_onto_entity_fast.tsv"
  metadata_file = open(os.path.join(cnst.code_path + metadata_fl_nm), 'w')
  metadata_file.write('Class\tName\n')

  for key in source_data.keys():
    embed_onto.append(source_data[key]['vector'])#for visualization purpose
    metadata_file.write('{}\t{}\n'.format(0, source_data[key]['lbl']+'_0'))# '0' for source ontology entities


  for key in target_data.keys():
    embed_onto.append(target_data[key]['vector'])#for visualization purpose
    metadata_file.write('{}\t{}\n'.format(1, target_data[key]['lbl']+'_1'))# '1' for target ontology entities

  metadata_file.close()

  embed_onto = np.asarray(embed_onto)
  features = tf.Variable(embed_onto, name='features')

  # local-machine (need tobe uncommented)
  # graph_path = tf.get_default_graph()
  graph_path = cnst.code_path + 'ontodata/util/graph'

  with tf.Session() as sess:
    saver = tf.train.Saver([features])

    sess.run(features.initializer)
    # we are saving because we can load the visualization later
    saver.save(sess, os.path.join(graph_path, 'entity_vec.ckpt'))

  print("Now run these following command")
  print("tensorboard --logdir="+graph_path+" -- port 6006")



#################### MAIN CODE START ####################
try:
    print("#################### EntityVecUtil START ####################")
    conf = assignVar()

    # plot Dictionary vector histogram
    test_fast_vec_viz = getFastVec(conf)
    plotFastTextDataFrequency(test_fast_vec_viz)

    # Plotting dictionary vectors
    plotTBEntity(conf)

except Exception:
    print(traceback.format_exc())
finally:
    print("#################### EntityVecUtil FINISH ####################")

#################### MAIN CODE END ####################