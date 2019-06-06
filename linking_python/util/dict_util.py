import json
import traceback
import numpy as np
import matplotlib.pyplot as plt
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from wordcloud import WordCloud

#load gloabal variables
colab_code_path = "/content/drive/My Drive/deep_learning/OntoSimilarity/"
code_path = colab_code_path
#local_code_path = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/FinalCode/GCP/OntoSimilarity/"
#code_path = local_code_path
#gcp_code_path = "/home/jaydeep_chakraborty_1988/research/OntoSimilarity/"
#code_path = gcp_code_path

def assignVar():
  
  conf = {
      'fl_nm_arr' : ['data/ip_op/source.json','data/ip_op/target.json']
  }

  return conf

def loadFile(conf):
  data = {}
  for conf_fl_nm in conf["fl_nm_arr"]:
    fl_nm = code_path+conf_fl_nm
    with open(fl_nm) as f:
      data.update(json.load(f))
      
  return data

def crtDictFreq(conf):
  
    onto_dict_freq = {}   
    data = loadFile(conf)
    for key in data.keys():
        words = data[key]['altLbl'].split()
        for word in words:
          if(word in onto_dict_freq):
            onto_dict_freq[word] = onto_dict_freq[word] + 1
          else:
            onto_dict_freq[word] = 1
    
    onto_dict_freq_sort = {k: v for k, v in sorted(onto_dict_freq.items(), key=lambda x: x[1],reverse=True)}
    return onto_dict_freq_sort

def plotLine(entity_dict_freq):
  output_notebook()
  x_axis_val = list(entity_dict_freq.keys())[0:80]
  y_axis_val = list(entity_dict_freq.values())[0:80]

  p = figure(y_range=(0, 500),x_range=x_axis_val,plot_width=800, plot_height=400)
  p.line(x=x_axis_val, y=y_axis_val, line_width=2)
  p.xaxis.major_label_orientation = np.pi/4
  show(p)

def plotWordCloud(entity_dict_freq):
#   entity_dict_freq = {k: entity_dict_freq[k] for k in list(entity_dict_freq)[:5]}
  

  text = " ".join([(k + " ")*v for k,v in entity_dict_freq.items()])
  
  wordcloud = WordCloud(background_color="white",collocations = False,stopwords=[])
  wordcloud.generate(text)
  plt.figure(figsize=(18, 30))
  plt.imshow(wordcloud, interpolation="bilinear")
  plt.axis("off")
  plt.show()

#################### MAIN CODE START ####################
try:
  
  conf = assignVar()
  entity_dict_freq = crtDictFreq(conf)
  
  #Plotting linegraph for frequency of each word in dictionary
#   plotLine(entity_dict_freq)
  
  #Plotting wordcloud of each word in dictionary
  plotWordCloud(entity_dict_freq)
  
#   for val in entity_dict_freq:
#     print(val, entity_dict_freq[val])
  
except Exception:
   print(traceback.format_exc())
finally:
  print("#################### FINISH ####################")
  
#################### MAIN CODE END ####################
