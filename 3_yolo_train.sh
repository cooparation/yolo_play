#!/bin/bash
./darknet -i 1 detector train \
    cfg/train_test_name.data \
    cfg/yolo-voc.cfg darknet19_448.conv.23
