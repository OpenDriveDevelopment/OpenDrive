import pandas as pd
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import random
import tensorflow as tf
from tqdm import tqdm
import datetime
from tensorflow import keras
from  matplotlib import pyplot as plt
import matplotlib.image as mpimg
from IPython.display import clear_output
from IPython.display import HTML
from base64 import b64encode

IMG_SIZE = 128
N_CHANNELS = 3 # RGB
N_CLASSES = 1
SEED = 123 # Random Seed

modelT = keras.models.load_model("cnn/model.h5")
