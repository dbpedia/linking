import nltk
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

import copy
import os
import re
import json
import traceback
import base64
import time
import datetime
import multiprocessing as mp
import scipy.spatial.distance

import numpy as np

import sys
import statistics

import operator
import math
from gensim.models import KeyedVectors

from fasttext import load_model

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api

from collections import OrderedDict

import keras
from keras import backend as K
from keras.models import Model, model_from_json
from keras.layers import Input, Dense, LSTM, concatenate, Reshape, Bidirectional, Flatten, Multiply, Activation, merge, RepeatVector, Permute, Lambda
from keras.utils.vis_utils import plot_model, model_to_dot
from keras.utils import plot_model
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

from zipfile import ZipFile