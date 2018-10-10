# --------------------------------------------------------
# Fast/er R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Bharath Hariharan
# --------------------------------------------------------

import xml.etree.ElementTree as ET
import os
import cPickle
import numpy as np


def parse_rec(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        # obj_struct['pose'] = obj.find('pose').text
        # obj_struct['truncated'] = int(obj.find('truncated').text)
        obj_struct['name'] = obj.find('name').text # get the class name
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)

    return objects


def voc_ap(rec, prec, use_07_metric=False):
    """ ap = voc_ap(rec, prec, [use_07_metric])
    Compute VOC AP given precision and recall.
    If use_07_metric is true, uses the
    VOC 07 11 point method (default:False).
    """
    if use_07_metric:
        # debug
        print("enter use_07_metric")
        # 11 point metric
        ap = 0.
        for t in np.arange(0., 1.1, 0.1):
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(prec[rec >= t])
            ap = ap + p / 11.
    else:
        # correct AP calculation
        # first append sentinel values at the end
        mrec = np.concatenate(([0.], rec, [1.]))
        mpre = np.concatenate(([0.], prec, [0.]))

        # compute the precision envelope
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def voc_eval(detpath,
             imagesetfile,
             classname,
             ovthresh,
             use_07_metric=False):
    """rec, prec, ap = voc_eval(detpath,
                                annopath,
                                imagesetfile,
                                classname,
                                [ovthresh],
                                [use_07_metric])

    Top level function that does the PASCAL VOC evaluation.

    detpath: Path to detections
        detpath.format(classname) should produce the detection results file.
    annopath: Path to annotations
        annopath.format(imagename) should be the xml annotations file.
    imagesetfile: Text file containing the list of images, one image per line.
    classname: Category name (duh)
    cachedir: Directory for caching the annotations
    [ovthresh]: Overlap threshold (default = 0.5)
    [use_07_metric]: Whether to use VOC07's 11 point AP computation
        (default False)
    """
    # assumes detections are in detpath.format(classname)
    # assumes annotations are in annopath.format(imagename)
    # assumes imagesetfile is a text file with each line an image name
    # cachedir caches the annotations in a pickle file

    
    # read list of images
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()

    imagePaths = [x.strip() for x in lines]
    # print("image name:", imagePaths)

    recs = {}
    for i, imgPath in enumerate(imagePaths):
        #xmlPath = imgPath.replace("images", "labels").replace("jpg", "xml")
        xmlPath = imgPath.replace("images", "Annotations").replace("jpg", "xml")
        recs[imgPath] = parse_rec(xmlPath)
        #print 'parse', xmlPath
        if i % 100 == 0:
            print "----- Reading annotation for {:d}/{:d}".format(i + 1, len(imgPath))

    # if not os.path.isfile(cachefile):
    #     # load annots
    #     recs = {}
    #     for i, imagename in enumerate(imagenames):
    #         recs[imagename] = parse_rec(annopath.format(imagename))
    #         if i % 100 == 0:
    #             print "Reading annotation for {:d}/{:d}".format(i + 1, len(imagenames))
    #     # save
    #     print 'Saving cached annotations to {:s}'.format(cachefile)
    #     with open(cachefile, 'w') as f:
    #         cPickle.dump(recs, f)
    # else:
    #     # load
    #     with open(cachefile, 'r') as f:
    #         recs = cPickle.load(f)

    # extract gt objects for this class
    class_recs = {}
    npos = 0
    for imagename in imagePaths:
        if classname == 'green_vegetable':
            xml_classname = 'green vegetable'
        else:
            xml_classname = classname
        R = [obj for obj in recs[imagename] if obj['name'] == xml_classname]
        bbox = np.array([x['bbox'] for x in R])
        difficult = np.array([x['difficult'] for x in R]).astype(np.bool)
        print 'difficult', difficult
        det = [False] * len(R)
        npos = npos + sum(~difficult)
        #print '------- imagename', imagename
        image_id = os.path.basename(imagename).split('.')[0]
        class_recs[image_id] = {'bbox': bbox,
                                 'difficult': difficult,
                                 'det': det}

    print '----- extract the object for each imagename -----'
    #print '------- class_recs', class_recs

    # read dets
    print 'detpath', detpath
    detfile = detpath.format(classname)
    print 'detfile', detfile
    with open(detfile, 'r') as f:
        lines = f.readlines()
        #print 'lines --- ' , lines

    splitlines = [x.strip().split(' ') for x in lines]
    image_ids = [x[0] for x in splitlines]
    #print("---- image_ids:",image_ids)
    confidence = np.array([float(x[1]) for x in splitlines])
    BB = np.array([[float(z) for z in x[2:]] for x in splitlines])

    # sort by confidence
    sorted_ind = np.argsort(-confidence)
    # modified if you want to set the thresh
    sorted_ind1 = np.where(confidence[sorted_ind] >= ovthresh)
    sorted_ind = sorted_ind[sorted_ind1]

    sorted_scores = np.sort(-confidence)
    BB = BB[sorted_ind, :]
    image_ids = [image_ids[x] for x in sorted_ind]

    # go down dets and mark TPs and FPs
    nd = len(image_ids)
    # debug
    print("classname:%s total:%d", classname, nd)
    tp = np.zeros(nd)
    fp = np.zeros(nd)

    cnt = 0

    print("ovthresh is:", ovthresh)
    
    iouDict = {}
    
    #print '\n class_recs', class_recs
    for d in range(nd):
        #print 'image_ids[d] ---', image_ids[d]
        R = class_recs[image_ids[d]]
        bb = BB[d, :].astype(float)
        ovmax = -np.inf
        BBGT = R['bbox'].astype(float)
        
        if image_ids[d] not in iouDict:
            iouDict[image_ids[d]] = []

        if BBGT.size > 0:
            # compute overlaps
            # intersection
            ixmin = np.maximum(BBGT[:, 0], bb[0])
            iymin = np.maximum(BBGT[:, 1], bb[1])
            ixmax = np.minimum(BBGT[:, 2], bb[2])
            iymax = np.minimum(BBGT[:, 3], bb[3])
            iw = np.maximum(ixmax - ixmin + 1., 0.)
            ih = np.maximum(iymax - iymin + 1., 0.)
            inters = iw * ih

            # union
            uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
                   (BBGT[:, 2] - BBGT[:, 0] + 1.) *
                   (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

            overlaps = inters / uni

            ovmax = np.max(overlaps)
            jmax = np.argmax(overlaps)
            

            if (d==0):
                print("overlaps is:", overlaps)
                print("jmax is:", jmax)

        if ovmax > 0.5:
            tp[d] = 1
            
            iouDict[image_ids[d]].append(jmax)
            # falseImg.append(image_ids[d])
            # if not R['difficult'][jmax]:
            #    if not R['det'][jmax]:
            #        tp[d] = 1.
            #        R['det'][jmax] = 1
            #    else:
            #        fp[d] = 1.
            #        falseImg.append(image_ids[d])
            #        print("false prediction in image %s"%image_ids[d])
        else:
            # if (image_ids[d] == "pic99"):
            #     cnt = cnt + 1
            fp[d] = 1.


    # tp_num is the number of TP objects after NMS
    tp_num = 0
    for img in iouDict:
        iouSet = set(iouDict[img])
        tmpNum = len(iouSet)
        tp_num = tmpNum+tp_num



    # print("pic99 appearence:", cnt)
    # print("false prediction in image ", set(falseImg))
    # compute precision recall
    # debug

    # fp = np.cumsum(fp)
    # tp = np.cumsum(tp)
    # rec = tp / float(npos)

    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)

    # ap = voc_ap(rec, prec, use_07_metric)
    # modified by juzhaoxue

    numfp = np.sum(fp)
    numtp = np.sum(tp)
    assert (numfp + numtp == nd)
    print("numtp:", numtp)
    print("numfp:", numfp)
    print("npos:", npos)

    #rec = numtp / float(npos)
    rec = tp_num / float(npos)
    ap = 1.0 * numtp / (numfp + numtp)

    return rec, prec, ap

