# YOLOV2 study project

## Deps
* git: https://github.com/pjreddie/darknet.git
* commit: 1e729804f61c8627eb257fba8b83f74e04945db7
* download pretrained models: curl -O https://pjreddie.com/media/files/darknet19_448.conv.23

## Usage
* Prepare Datasets: images and labels
* create soft links with some bins of darknet
* convert_xml_txt: if the label files are similar with VOC xml label data, the step of converting xml to txt format that darknet can be used is needed
* write test, train and class name lists

## Outputs
* backup: the weights generated
* bad.list: bad list images
* predictions.jpg

## Net instruction
* ``http://www.cnblogs.com/hansjorn/p/7491391.html``  
