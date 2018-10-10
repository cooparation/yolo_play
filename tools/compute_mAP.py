#!/usr/bin/env python

# Adapt from ->
# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------
# <- Written by Yaping Sun

"""Reval = re-eval. Re-evaluate saved detections."""

import os, sys, argparse
import numpy as np
import cPickle

from voc_eval import voc_eval

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Re-evaluate results')
    parser.add_argument('output_dir', nargs=1, help='results directory',
                        type=str)

    parser.add_argument('--imageset_txt', dest='imageset_txt', default='./valid.txt', type=str)

    parser.add_argument('--classes', dest='class_file', default='./test_food/food.names', type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

def get_voc_results_file_template(out_dir = 'results'):
    filename = 'comp4_det_' + "test" + '_{:s}.txt'
    path = os.path.join(out_dir, filename)
    return path

def do_python_eval(image_set, classes, confi_thresh, static_result, output_dir = 'results'):
    imagesetfile = image_set
    #cachedir = os.path.join(devkit_path, 'annotations_cache')
    aps = []
    # The PASCAL VOC metric changed in 2010
    # use_07_metric = True if int(year) < 2010 else False
    use_07_metric = True
    print 'VOC07 metric? ' + ('Yes' if use_07_metric else 'No')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    static_result.write(str(confi_thresh))
    static_result.write("\n")
    for i, cls in enumerate(classes):
        if cls == '__background__':
            continue
        filename = get_voc_results_file_template().format(cls)
        rec, prec, ap = voc_eval(
            filename, imagesetfile, cls, ovthresh=confi_thresh,
            use_07_metric=use_07_metric)
        aps += [ap]

        static_result.write("{} AP = {:.4f}  REC = {:.4f}\n".format(cls, ap, rec))
        # print('AP for {} = {:.4f}'.format(cls, ap))
        # with open(os.path.join(output_dir, cls + '_pr.pkl'), 'w') as f:
        #     cPickle.dump({'rec': rec, 'prec': prec, 'ap': ap}, f)

    static_result.write('Mean AP = {:.4f}\n'.format(np.mean(aps)))

    # print('Mean AP = {:.4f}'.format(np.mean(aps)))
    # print('~~~~~~~~')
    # print('Results:')
    # for ap in aps:
    #     print('{:.3f}'.format(ap))
    # print('{:.3f}'.format(np.mean(aps)))
    # print('~~~~~~~~')
    # print('')
    # print('--------------------------------------------------------------')
    # print('Results computed with the **unofficial** Python eval code.')
    # print('Results should be very close to the official MATLAB eval code.')
    # print('-- Thanks, The Management')
    # print('--------------------------------------------------------------')


if __name__ == '__main__':
    # args = parse_args()
    #
    # output_dir = os.path.abspath(args.output_dir[0])
    # with open(args.class_file, 'r') as f:
    #     lines = f.readlines()
    #
    # classes = [t.strip('\n') for t in lines]
    #
    # print 'Evaluating detections'
    # do_python_eval(args.imageset_txt, classes, output_dir)

    imageset_txt = "tmp/food_830/data/train_val.txt"
    output_dir = "./results"
    class_file = "./tmp/food_830/food_lists.names"
    with open(class_file, "rb") as f:
        lines = f.readlines()

    classes = [t.strip("\n") for t in lines]

    static_result = open("static.txt","a")
    for thresh in np.arange(0.4, 0.8, 0.05):
        do_python_eval(imageset_txt, classes, thresh, static_result, output_dir)
