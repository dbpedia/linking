import sys
sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst


import matplotlib.pyplot as plt
import tensorflow as tf


def assignVar():
  conf = {
    'dict_json': 'ontodata/dict/dict_fast.json',
    'dict_vec_hist': 'ontodata/util/dict_vec_hist.png'
  }

  return conf


def getFastVec(conf):
  dict_fl_nm = cnst.code_path + conf['dict_json']
  with open(dict_fl_nm) as f:
    fast_entity_dict = json.load(f)

  fast_vec_viz = []
  for i in fast_entity_dict:
    fast_vec_viz.append(fast_entity_dict[i])

  return np.asarray(fast_vec_viz)


def plotFastTextDataFrequency(encoded_entity):
    print(encoded_entity.shape)
    print("min:- "+str(np.nanmin(encoded_entity))+" max:- "+str(np.nanmax(encoded_entity)))
    flat_encoded_entity = encoded_entity.flatten()
    print(flat_encoded_entity.shape)

    plt.hist(flat_encoded_entity, bins = [-6,-5,-4,-3,-2,-1,-.9,-.8,-.7,-.6,-.5,
                                          -.4,-.3,-.2,-.1,0,.1,.2,.3,.4,.5,.6,.7,
                                          .8,.9,1,2,3,4,5,6]) 

    plt.title("Dictionary FastText vector histogram")
    plt.savefig(os.path.join(cnst.code_path + conf['dict_vec_hist']))


def plotTBEntity(conf):

  dict_fl_nm = cnst.code_path + conf['dict_json']
  with open(dict_fl_nm) as f:
    dict_data = json.load(f)

  seed = 43
  tf.reset_default_graph()
  tf.set_random_seed(seed)
  np.random.seed(seed)

  embed_onto = []  # for visualization purpose

  metadata_fl_nm = "ontodata/util/metadata_onto_dict_fast.tsv"
  metadata_file = open(os.path.join(cnst.code_path + metadata_fl_nm), 'w')

  for key in dict_data.keys():
    embed_onto.append(dict_data[key])  # for visualization purpose
    metadata_file.write('{}\n'.format(key))

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
    saver.save(sess, os.path.join(graph_path, 'dict_vec.ckpt'))

  print("Now run these following command")
  print("tensorboard --logdir="+graph_path+" -- port 6006")



#################### MAIN CODE START ####################
try:
    print("#################### DictVecUtil START ####################")
    conf = assignVar()

    # plot Dictionary vector histogram
    test_fast_vec_viz = getFastVec(conf)
    plotFastTextDataFrequency(test_fast_vec_viz)

    # Plotting dictionary vectors
    plotTBEntity(conf)

except Exception:
    print(traceback.format_exc())
finally:
    print("#################### DictVecUtil FINISH ####################")

#################### MAIN CODE END ####################