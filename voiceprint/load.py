#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @File    : load.py
# @Author  : Lonen
# @Email   : 17621302715@163.com
# @Time    : 2018/7/30 14:26


from keras.models import Model

from keras.models import load_model
from ai import settings
import tensorflow as tf


def init():
    print("model loading...")
    loaded_model = load_model(settings.MODEL_PATH)
    print("model loaded.")
    inter_model = Model(inputs=loaded_model.input, outputs=loaded_model.get_layer('dnsthree').output)
    graph = tf.get_default_graph()
    return inter_model, graph
