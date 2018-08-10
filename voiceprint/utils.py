#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @File    : utils.py
# @Author  : Lonen
# @Email   : 17621302715@163.com
# @Time    : 2018/8/9 16:33
import numpy as np

nchannels = 1
sampwidth = 2
framerate = 8000

window_length = 100
window_amplitude = 500
silding_length = 5
wave_length = 2400
threshold = 1000


def get_start_point(wave_data, window_length=100, silding_length=5, threshold=1000):
    '''
    利用均值滤波的方法获取起始点
    :param wave_data: 音频数据
    :param window_length: 窗宽
    :param silding_length: 滑动间隔
    :param threshold: 阈值
    :return: 起始点
    '''
    
    sin_window = np.sin(np.linspace(0, np.pi, window_length)) * window_amplitude
    wave_data_abs = np.abs(wave_data)
    for i in np.arange(0, wave_data_abs.size - window_length, silding_length):
        data_window = wave_data_abs[i:i + window_length]
        mask = sin_window > data_window
        diff = sin_window - data_window
        if np.sum(diff[mask]) <= threshold:
            start_point = i
            break
    else:
        print("未找到起始点")
        raise Exception("未找到起始点")
    return start_point
