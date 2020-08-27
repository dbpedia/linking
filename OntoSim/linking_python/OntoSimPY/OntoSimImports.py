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
import scipy.spatial.distance

import numpy as np

import sys
import statistics
import math

import fasttext
import fasttext.util
from fasttext import load_model

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api

from collections import OrderedDict

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

from sklearn.preprocessing import MinMaxScaler

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

from zipfile import ZipFile

from pprint import pprint
