# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

xmlLabel_Dir = '/home/liusj/deepLearning/ssd_play/testLabelImgs/Annotations'

classes = ["toast"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

if not os.path.exists('labels/'):  #生成的label放在label目录下
    os.makedirs('labels/')
for rootDir,dirs,files in os.walk(xmlLabel_Dir):
    for file in files:
        file_name = file.split('.')[0]
        out_file = open('labels/%s.txt'%(file_name),'w')
        in_file = open("%s/%s"%(rootDir,file))
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult)==1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.close()
