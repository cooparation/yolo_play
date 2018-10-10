#!/bin/bash
# first to modify the function with named validate_detector_recall in example/detector.c
# list *plist = get_paths("data/coco_val_5k.list");
# the recall test results:
#       Number Correct Total Rps/Img           IOU          Recall
#         289   710    746   RPs/Img: 21.33  IOU: 75.44% Recall:95.17%
./darknet detector recall cfg/voc.data cfg/tiny-yolo.cfg backup/tiny-yolo-voc_final.weights
