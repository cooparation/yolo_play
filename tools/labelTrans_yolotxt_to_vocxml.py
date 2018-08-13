# -*- coding: utf-8 -*-
#! /usr/bin/python

import os, sys
import glob
from PIL import Image

# ground truth 文件格式为：xmin, ymin, xmax, ymax, label
# 158,128,412,182,"labelName"

# ICDAR 图像存储位置
src_img_dir = "./testTXT/Images"
# ICDAR 图像的 ground truth 的 txt 文件存放位置
src_txt_dir = "./testTXT/Images"
src_voc_dir = "./testVOC"
classes = ["face", "fist", "palm"]

img_Lists = glob.glob(src_img_dir + '/*.jpg')

img_basenames = [] # e.g. 100.jpg
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

img_names = [] # e.g. 100
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)

for img in img_names:
    im = Image.open((src_img_dir + '/' + img + '.jpg'))
    width, height = im.size

    # open the crospronding txt file
    gt = open(src_txt_dir + '/' + img + '.txt').read().splitlines()

    # write in xml file
    os.mknod(src_voc_dir + '/' + img + '.xml')
    xml_file = open((src_voc_dir + '/' + img + '.xml'), 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    # write the region of text on xml file
    for img_each_label in gt:
        spt = img_each_label.split(' ')
        print spt[1]
        print spt[2]

        #YOLO data
        tmpx = float(spt[1]) *width*2
        tmpy = float(spt[2]) *height*2
        tmpw = float(spt[3]) *width
        tmph = float(spt[4]) *height
        x = int((tmpx - tmpw )/2)
        y = int((tmpx + tmpw )/2)
        w = int((tmpy - tmph )/2)
        h = int((tmpy + tmph )/2)
        text = classes[int(spt[0])]

        xml_file.write('    <object>\n')
        xml_file.write('        <name>' + text + '</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        #xml_file.write('            <xmin>' + str(spt[0]) + '</xmin>\n')
        #xml_file.write('            <ymin>' + str(spt[1]) + '</ymin>\n')
        #xml_file.write('            <xmax>' + str(spt[2]) + '</xmax>\n')
        #xml_file.write('            <ymax>' + str(spt[3]) + '</ymax>\n')
        xml_file.write('            <xmin>' + str(x) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(y) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(w) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(h) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')

    xml_file.write('</annotation>')
