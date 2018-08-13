#!/bin/bash
./darknet detector train \
    cfg/train_test_name.data \
    cfg/yolov3-tiny.cfg ./pretrained_models/yolo/yolov3-tiny.weights \
    -gpus 0,1,2,3 >>log.txt
