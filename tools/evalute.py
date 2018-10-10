# coding=utf-8
# this tool can be used with category command
# category is a new parameter added to detector.c, which helps to generate each class evalute result
# run following: ./darknet detector category cfg/paul.data cfg/yolo-paul.cfg backup/yolo-paul_final.weights
# the each class val result will be put into result dir, if you run this tool at result dir, the evalute results will be printed, including
# id,avg_iou,avg_correct_iou,avg_precision,avg_recall,avg_score
# result the low_list and high_list will be generated into result dir，the contents is the accuace and the recall of true and false classes

import os
from os import listdir, getcwd
from os.path import join
import shutil


# validate result of each category
class CategoryValidation:
    id = 0  # Category id
    path = ""  # path
    total_num = 0  # the total bounding box num in labeled files
    proposals_num = 0  # validate results predict the total num bounding box at this category
    correct_num = 0  # the num of true bounding box that predicted(based on the IOU greater 0.5 and the category predict correct)
    iou_num = 0  # the total num of IOU greater 0.5
    iou_sum = 0  # the sum of the total num of IOU greater 0.5
    correct_iou_sum = 0  # the total num of correct predicted bounding box
    score_sum = 0  # the sum of score that correctly predicted bounding box
    avg_iou = 0  # no matter the bounding box of object is predicted corrected, all the bounding box match Ground-truth best and get IOU, then for the IOU greater 0.5, calculate the avg ad: avg_iou = iou_sum/iou_num
    avg_correct_iou = 0  # avg the correct predicted bounding box IOU：avg_correct_iou = correct_iou_sum/correct_num
    avg_precision = 0  # avg_precision = correct_num/proposals_num
    avg_recall = 0  # avg_recall = correct_num/total_num
    avg_score = 0  # avg_score=score_sum/correct_num

    def __init__(self, path, val_cat_num):
        self.path = path
        f = open(path)

        for line in f:
            temp = line.rstrip().replace(' ', '').split(',', 9)
            temp[1] = int(temp[1])
            self.id = temp[1]
            self.total_num = val_cat_num[self.id]
            if (self.total_num):
                break

        for line in f:
            # path, class_id, correct, prob, best_iou, xmin, ymin, xmax, ymax
            temp = line.rstrip().split(', ', 9)
            temp[1] = int(temp[1])
            temp[2] = int(temp[2])
            temp[3] = float(temp[3])
            temp[4] = float(temp[4])
            self.proposals_num = self.proposals_num + 1.00
            if (temp[2]):
                self.correct_num = self.correct_num + 1.00
                self.score_sum = self.score_sum + temp[3]
                self.correct_iou_sum = self.correct_iou_sum + temp[4]
            if (temp[4] > 0.5):
                self.iou_num = self.iou_num + 1
                self.iou_sum = self.iou_sum + temp[4]

        self.avg_iou = self.iou_sum / self.iou_num
        self.avg_correct_iou = self.correct_iou_sum / self.correct_num
        self.avg_precision = self.correct_num / self.proposals_num
        self.avg_recall = self.correct_num / self.total_num
        self.avg_score = self.score_sum / self.correct_num

        f.close()

    # save the correctly predicted image list
    def get_correct_list(self):
        f = open(self.path)
        new_f_name = "correct_list_" + self.id + ".txt"
        new_f = open(new_f_name, 'w')
        for line in f:
            temp = line.rstrip().split(', ', 9)
            if (temp[2]):
                new_f.write(line)
        f.close()

    # save the wrong predicted image list
    def get_error_list(self):
        f = open(self.path)
        new_f_name = "error_list_" + self.id + ".txt"
        new_f = open(new_f_name, 'w')
        for line in f:
            temp = line.rstrip().split(', ', 9)
            if (temp[2] == 0):
                new_f.write(line)
        f.close()

    def print_eva(self):
        print("id=%d, avg_iou=%f, avg_correct_iou=%f, avg_precision=%f, avg_recall=%f, avg_score=%f \n" % (self.id,
                                                                                                           self.avg_iou,
                                                                                                           self.avg_correct_iou,
                                                                                                           self.avg_precision,
                                                                                                           self.avg_recall,
                                                                                                           self.avg_score))


def IsSubString(SubStrList, Str):
    flag = True
    for substr in SubStrList:
        if not (substr in Str):
            flag = False

    return flag


# get the file name list in path of FindPath which format with FlagStr
def GetFileList(FindPath, FlagStr=[]):
    import os
    FileList = []
    FileNames = os.listdir(FindPath)
    if (len(FileNames) > 0):
        for fn in FileNames:
            if (len(FlagStr) > 0):
                if (IsSubString(FlagStr, fn)):
                    FileList.append(fn)
            else:
                FileList.append(fn)

    if (len(FileList) > 0):
        FileList.sort()

    return FileList


# get the total num of ROI for all the object classes
# path is the file of image name list
# return a list，the index of list is the id of object class,
#           the value is the ROI num of this object class
def get_val_cat_num(path, class_num):
    val_cat_num = []
    for i in range(0, class_num):
        val_cat_num.append(0)

    f = open(path)
    for line in f:
        label_path = line.rstrip().replace('images', 'labels')
        label_path = label_path.replace('JPEGImages', 'labels')
        label_path = label_path.replace('.jpg', '.txt')
        label_path = label_path.replace('.JPEG', '.txt')
        label_list = open(label_path)
        for label in label_list:
            temp = label.rstrip().split(" ", 4)
            id = int(temp[0])
            val_cat_num[id] = val_cat_num[id] + 1.00
        label_list.close()
    f.close()
    return val_cat_num


# get object name list
# path is the object file list
# return a list，the index of list is the id of object class, the value is the ROI num of this object class
def get_name_list(path):
    name_list = []
    f = open(path)
    for line in f:
        temp = line.rstrip().split(',', 2)
        name_list.append(temp[1])
    return name_list


# the total class num
class_num = 97
wd = getcwd()

val_result_list = GetFileList(wd, ['txt'])
val_cat_num = get_val_cat_num("/raid/pengchong_data/Data/filelists/val.txt", class_num)
name_list = get_name_list("/raid/pengchong_data/Tools/Paul_YOLO/data/paul_list.txt")
low_list = open("low_list.log", 'w')
high_list = open("high_list.log", 'w')
for result in val_result_list:
    cat = CategoryValidation(result, val_cat_num)
    cat.print_eva()
    if ((cat.avg_precision < 0.3) | (cat.avg_recall < 0.3)):
        low_list.write("id=%d, name=%s, avg_precision=%f, avg_recall=%f \n" % (cat.id, name_list[cat.id], cat.avg_precision, cat.avg_recall))
    if ((cat.avg_precision > 0.6) & (cat.avg_recall > 0.6)):
        high_list.write("id=%d, name=%s, avg_precision=%f, avg_recall=%f \n" % (cat.id, name_list[cat.id], cat.avg_precision, cat.avg_recall))

low_list.close()
high_list.close()
