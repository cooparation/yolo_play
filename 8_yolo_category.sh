#!/bin/bash
# get each class the val result and save it to each txt file, the txt file
#  contents is: path, class_id, correct, prob, best_iou, xmin, ymin, xmax, ymax
# then use the tools/evalute.py get analysis it
./darknet detector category cfg/voc.data cfg/yolo-voc.cfg backup/yolo-voc_final.weights
