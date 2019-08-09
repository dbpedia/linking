import sys
sys.path.append("./")

from OntoSimImports import *
import OntoSimConstants as cnst


import matplotlib.pyplot as plt
from bokeh.io import output_notebook, export_svgs
from bokeh.plotting import figure, show, output_file, save
from wordcloud import WordCloud


def assignVar():
    conf = {
        'fl_nm_arr': ['ontodata/modifylbl/source.json',
                      'ontodata/modifylbl/target.json'],
        'dict_freq_line': 'ontodata/util/dict_freq.html',
        'dict_freq_wc': 'ontodata/util/dict_word_cloud.png'
    }

    return conf


def loadFile(conf):
    data = {}
    for conf_fl_nm in conf["fl_nm_arr"]:
        fl_nm = cnst.code_path + conf_fl_nm
        with open(fl_nm) as f:
            data.update(json.load(f))

    return data


def crtDictFreq(conf):
    onto_dict_freq = {}
    data = loadFile(conf)
    for key in data.keys():
        words = data[key]['altLbl'].split()
        for word in words:
            if (word in onto_dict_freq):
                onto_dict_freq[word] = onto_dict_freq[word] + 1
            else:
                onto_dict_freq[word] = 1

    onto_dict_freq_sort = {k: v for k, v in sorted(onto_dict_freq.items(), key=lambda x: x[1], reverse=True)}
    return onto_dict_freq_sort


def plotLine(entity_dict_freq):
    # output_notebook()
    x_axis_val = list(entity_dict_freq.keys())[0:80]
    y_axis_val = list(entity_dict_freq.values())[0:80]

    p = figure(y_range=(0, 500), x_range=x_axis_val, plot_width=800, plot_height=400)
    p.line(x=x_axis_val, y=y_axis_val, line_width=2)
    p.xaxis.major_label_orientation = np.pi / 4
    p.xaxis.axis_label = "Words"
    p.yaxis.axis_label = "Frequency"
    output_file(cnst.code_path + conf["dict_freq_line"])
    save(p)


def plotWordCloud(entity_dict_freq):
    #   entity_dict_freq = {k: entity_dict_freq[k] for k in list(entity_dict_freq)[:5]}

    text = " ".join([(k + " ") * v for k, v in entity_dict_freq.items()])

    wordcloud = WordCloud(background_color="white", collocations=False, stopwords=[])
    wordcloud.generate(text)
    plt.figure(figsize=(18, 30))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    plt.savefig(cnst.code_path + conf["dict_freq_wc"])


#################### MAIN CODE START ####################
try:
    print("#################### DictUtil START ####################")
    conf = assignVar()
    entity_dict_freq = crtDictFreq(conf)

    # Plotting linegraph for frequency of each word in dictionary
    plotLine(entity_dict_freq)

    # Plotting wordcloud of each word in dictionary
    plotWordCloud(entity_dict_freq)

#   for val in entity_dict_freq:
#     print(val, entity_dict_freq[val])

except Exception:
    print(traceback.format_exc())
finally:
    print("#################### DictUtil FINISH ####################")

#################### MAIN CODE END ####################
