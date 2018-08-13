#!/bin/bash
GPU=1
./darknet -i 1 detector test \
    cfg/train_test_name.data cfg/yolov3-tiny.cfg \
    /apps/liusj/backup/yolov3-tiny_40000.weights \
    /apps/liusj/datasets/handDatasets/Images/Palm_0572.jpg

#./darknet detect \
#    cfg/yolov3-tiny.cfg \
#    /apps/liusj/backup/yolov3-tiny_40000.weights \
#    /apps/liusj/datasets/handDatasets/Images/Palm_0572.jpg

# webcam demo
#./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights
