#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @File    : predict.py
# @Author  : Lonen
# @Email   : 17621302715@163.com
# @Time    : 2018/7/30 11:16

import numpy as np
from scipy.io import wavfile

from python_speech_features import mfcc
import sys
from functools import reduce
# from voiceprint.load import init

from keras.models import Model

from keras.models import load_model
from ai import settings
import tensorflow as tf
from voiceprint.utils import get_start_point


# outputs_layer = 'dnsone'


def init():
    global model, graph
    print("model loading...")
    loaded_model = load_model(settings.MODEL_PATH)
    print("model loaded.")
    model = Model(inputs=loaded_model.input, outputs=loaded_model.get_layer(settings.outputs_layer).output)
    graph = tf.get_default_graph()


init()


# 加载模型
# def get_model(model_path):
#     model = load_model(model_path)
#     inter_model = Model(inputs=model.input, outputs=model.get_layer('dnsthree').output)
#     return inter_model


# 数据预处理（mfcc)
def preprocess(wav_path):
    sr, audio_data = wavfile.read(wav_path)
    start_point = get_start_point(audio_data)
    mfcc_data = mfcc(audio_data[start_point:start_point + 8000], sr)
    mfcc_data = mfcc_data[np.newaxis, :, :, np.newaxis]
    mfcc_data = np.abs(mfcc_data) / 100.0
    return mfcc_data


# v1_v2_norm = np.linalg.norm(v_1 - v_2)
# v1_norm = np.linalg.norm(v_1)
# v1_norm = np.linalg.norm(v_2)
# 计算两个向量的距离
def distance(v_1, v_2):
    v1_norm = np.sqrt(np.sum(v_1 * v_1))
    v2_norm = np.sqrt(np.sum(v_2 * v_2))
    # v1_norm = np.linalg.norm(v_1)
    # v2_norm = np.linalg.norm(v_2)
    v1_v2_norm = np.sum(v_1 * v_2)
    dist = v1_v2_norm / (v1_norm * v2_norm)
    return dist


def encoding(wav_path):
    return model.predict(preprocess(wav_path))


def verify(audio):
    with graph.as_default():
        d = reduce(distance, list(map(encoding, audio)))
        return d.item()


if __name__ == '__main__':
    _, model_path, audio = sys.argv
    audio = audio.split(',')
    verify(model_path, audio)
