# coding=utf-8
# this toool is used to statistic the dataset image num and ROI num for each class
# it will generate num_list.log, the content is id，name，ROI_num image_num
# it will generate less_list.log, the content is the id, name ROI_num and image_num
# that the image number less 1000

import os
from os import listdir, getcwd
from os.path import join
import shutil

# get the label list
# path is image path list
# return a list, which save all the label file path lists
def get_label_path_list(path):
    label_path_list = []
    f = open(path)
    for line in f:
        label_path = line.rstrip().replace('images', 'labels')
        label_path = label_path.replace('JPEGImages', 'labels')
        label_path = label_path.replace('.jpg', '.txt')
        label_path = label_path.replace('.JPEG', '.txt')
        label_path_list.append(label_path)
    return label_path_list


# get each class ROI nums
# label_path_list is the label file list
# return a list, the index is class id, the value is ROI num of the class
def get_cat_roi_num(label_path_list, class_num):
    val_cat_num = []
    for i in range(0, class_num):
        val_cat_num.append(0)

    for line in label_path_list:
        label_list = open(line)
        for label in label_list:
            temp = label.rstrip().split(" ", 4)
            id = int(temp[0])
            val_cat_num[id] = val_cat_num[id] + 1
        label_list.close()
    return val_cat_num


# get the image num for each class
# label_path_list is label file list
# return a list, the index is class id, the value is image num of the class
def get_cat_file_num(label_path_list, class_num):
    val_cat_num = []

    for i in range(0, class_num):
        val_cat_num.append(0)

    for line in label_path_list:
        label_list = open(line)

        flags = []
        for i in range(0, class_num):
            flags.append(0)

        for label in label_list:
            id = int(label.rstrip().split(" ", 4)[0])
            if (id < class_num):
                flags[id] = 1

        for i in range(0, class_num):
            if (flags[i] == 1):
                val_cat_num[i] = val_cat_num[i] + 1

        label_list.close()
    return val_cat_num


# get class name list
# path is the object list path
# return a list, the index is class id, the value is class name
def get_name_list(path):
    name_list = []
    f = open(path)
    for line in f:
        #temp = line.rstrip().split(',', 2)
        #name_list.append(temp[1])
        temp = line.rstrip().split()
        name_list.append(temp[0])
        print 'Class:', temp[0]
    return name_list


# the total class num
class_num = 3

image_list_path = "./data/test_fridge.txt"
label_path_list = get_label_path_list(image_list_path)
name_list_file = "./tmp/food_lists.names"
name_list = get_name_list(name_list_file)
cat_roi_num = get_cat_roi_num(label_path_list, class_num)
cat_file_num = get_cat_file_num(label_path_list, class_num)

num_list = open("num_list.log", 'w')
less_list = open("less_list.log", 'w')

num_list.write("id name roi_num image_num\n")
less_list.write("id name roi_num image_num\n")
for i in range(0, class_num):
    print 'Class', i
    num_list.write("%d, %s, %d, %d \n" % (i, name_list[i], cat_roi_num[i], cat_file_num[i]))
    if (cat_file_num[i] < 1000):
        less_list.write("%d, %s, %d, %d \n" % (i, name_list[i], cat_roi_num[i], cat_file_num[i]))

num_list.close()
less_list.close()

