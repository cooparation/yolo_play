#!/bin/bash
# the voc.data should be contained the valid option to supply 
#  the image path, details to see cfg/train_test_name.data
if [ ! -d "./results/" ];then
    mkdir ./results
else
    echo "the results is exist"
fi
./darknet detector valid  \
    ./cfg/voc.data \
    cfg/tiny_yolo_voc.cfg \
    tiny_yolo_voc.weights

python ./tools/reval_voc.py --voc_dir VOCdevkit --year 2007 --image_set test --class ./data/voc.names .
