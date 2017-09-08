#!/bin/bash
./darknet -i 1 detector test \
    cfg/train_test_name.data cfg/yolo-voc.cfg \
    ./backup/yolo-voc_10000.weights \
    images/20170724173238.jpg
