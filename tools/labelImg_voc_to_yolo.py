# coding=utf-8

###################################
# instruction
# the struct of dir to trans：
# Paul/time/class/annotations/[xml files]
# Paul/time/class/images/[jpg files]
# Paul/time/class/labels/[the generated yolo txt files]

# the files are contained in Paul, the name with “date” txt files，which
# contains is the path of all date dir

# how many directories of the time, how many names of the directories
# will be added into the sets

# the labels to be added into classes
# in labels txt file, the first num is class index
###################################


import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil
from collections import OrderedDict


###################################
# Brief: get class name and id
# path is a menu list file for the relationship between class-name and id,
#      and we only load the class the menu list file pointed
# return dictionary which key is class-name and value is id
def get_classes_and_index(path):
    D = {}
    f = open(path)
    for line in f:
        temp = line.rstrip().split(',', 2)
        print("temp[0]:" + temp[0] + "\n")
        print("temp[1]:" + temp[1] + "\n")
        D[temp[1].replace(' ', '')] = temp[0]
    print 'classes name id:', D
    return D

###################################
# Brief: convert ROI to yolo labels
# size is the image w and h
# box is the ROI coodinate(the max and min value of x and y)
# return the center of ROI rate cooresponding with image width and height,
#        and the w,h which is alse the rate for image width and height
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

###################################
# Brief: convert labelImg xml files to yolo txt files
# path contains the JPEGImages, Annotations and labels directories
# image_id is the image name without the suffix
def convert_annotation(path, image_id, classes):
    in_file = open('%s/Annotations/%s.xml' % (path, image_id))
    out_file = open('%s/labels/%s.txt' % (path, image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text #.replace(' ', '')
        # if the class is not in the list of training, it will be ignored
        # the type dictionary of classes should be perpared firstly
        if cls not in classes:
            continue

        #cls_id = classes[cls]  # get the class id
        cls_id = classes.index(cls)  # get the class id

        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    out_file.close()


def IsSubString(SubStrList, Str):
    flag = True
    for substr in SubStrList:
        if not (substr in Str):
            flag = False

    return flag


# from FindPath to get pointed format (FlagStr) file name lists(not include the suffix)
def GetFileList(FindPath, FlagStr=[]):
    import os
    FileList = []
    FileNames = os.listdir(FindPath)
    if (len(FileNames) > 0):
        for fn in FileNames:
            if (len(FlagStr) > 0):
                if (IsSubString(FlagStr, fn)):
                    FileList.append(fn[:-4])
            else:
                FileList.append(fn)

    if (len(FileList) > 0):
        FileList.sort()

    return FileList

# get the sub contents lists of the time content
def get_dirs(time):
    dirs = []
    dirs_temp = os.listdir(time)
    for dir_name in dirs_temp:
        dirs.append(time + '/' + dir_name)
    return dirs


# sets = [ './data/VOCdevkit'] 
# the sets dirs containes [VOC2007  VOC2012] 
sets = [
        '/workspace/D2/sanjun/ExtractedVOCClasses'
        ]

#classes = get_classes_and_index('./tmp/class-name_id.txt')
#classes = OrderedDict()
#classes['person'] = [0]
classes = ['person']

for time in sets:
    dirs = get_dirs(time)
    list_file = open('%s.txt' % time, 'w')  # the image data list save dirs
    for path in dirs:
        if not os.path.isdir(path):
            continue
        print 'path:', path
        #if not os.path.exists('%s/annotations/' % path):
        #    os.makedirs('%s/annotations/' % path)
        if not os.path.exists('%s/images/' % path):
            os.makedirs('%s/images/' % path)
        if not os.path.exists('%s/labels/' % path):
            os.makedirs('%s/labels/' % path)
        else:
            shutil.rmtree('%s/labels/' % path)
            os.makedirs('%s/labels/' % path)
            saveImagesPath = os.path.join(path, 'images')
        image_ids = GetFileList(path + '/Annotations/', ['xml'])
        for image_id in image_ids:
            list_file.write('%s/images/%s.jpg\n' % (path, image_id))
            convert_annotation(path, image_id, classes)
            imagePath = os.path.join(path, 'JPEGImages', image_id + '.jpg')
            savePath = os.path.join(path, 'images')
            shutil.copy(imagePath, savePath)
            print "copy", imagePath, " --> ", savePath
    list_file.close()
