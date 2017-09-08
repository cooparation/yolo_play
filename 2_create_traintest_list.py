# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from random import shuffle

TrainImgDir = '/home/liusj/deepLearning/yolov2_play/images'

write_lines = []
for root,dirs,files in os.walk(TrainImgDir):
    imgnum = 0
    for file in files:
        imgnum += 1
        filename = root + '/' + file
        filename += '\n'
        write_lines.append(filename)

shuffle(write_lines)

L = int(len(write_lines) * 0.1)

test_file = open('data/test.txt','w')
test_file.writelines(write_lines[:L])
test_file.close()

train_file = open('data/train.txt','w')
train_file.writelines(write_lines[:L])
train_file.close()
