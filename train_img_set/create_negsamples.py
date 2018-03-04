#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'qxr'


import cv2
import os
import os.path
import sys
import numpy as np

def readfile(filename):
    file_rects = {}
    with open(filename) as f:
        lines = f.readlines()
        idx = 0
        while idx < len(lines):
            image_name = lines[idx].strip()
            idx += 1
            num_boxes = int(lines[idx])
            bboxs = []
            for i in xrange(num_boxes):
                idx += 1
                coor = map(float, lines[idx].split())
                x1 = coor[0]
                y1 = coor[1]
                x2 = x1 + coor[2] - 1.
                y2 = y1 + coor[3] - 1.
                bboxs.append([x1, y1, x2, y2])
            file_rects[image_name] = np.array(bboxs)
            idx += 1

        assert (idx == len(lines))
    return file_rects

def create_negsamples(datapath, gtfile, imagefile, neglist):
    nonface_id = 0
    fid = open(neglist, 'w')
    with open(imagefile) as f:
        lines = f.readlines()
    imagelist = [x.strip() for x in lines]
    gt_rects = readfile(gtfile)
    assert (len(gt_rects) == len(imagelist))

    for imagename in imagelist:
        print 'Processing ' + imagename
        enough = 0
        gt_bbox = gt_rects[imagename]
        ngt = len(gt_bbox)

        image_path = os.path.join(datapath, imagename)
        img = cv2.imread(image_path)
        imw = img.shape[1]
        imh = img.shape[0]
        cn = min(imw / 100, imh / 100)
        for i in xrange(cn/5, cn*4/5):
            for j in xrange(cn/5, cn*4/5):
                print i, j
                c_bbox = [j*100, i*100, j*100+99, i*100+99]
                nonface_flag = 1
                if ngt > 0:
                    xmin = np.maximum(gt_bbox[:, 0], c_bbox[0])
                    ymin = np.maximum(gt_bbox[:, 1], c_bbox[1])
                    xmax = np.minimum(gt_bbox[:, 2], c_bbox[2])
                    ymax = np.minimum(gt_bbox[:, 3], c_bbox[3])
                    iw = np.maximum(xmax - xmin + 1., 0.)
                    ih = np.maximum(ymax - ymin + 1., 0.)
                    inter = iw * ih
                    union = (100 * 100 + (gt_bbox[:, 2] - gt_bbox[:, 0] + 1.) *
                             (gt_bbox[:, 3] - gt_bbox[:, 1] + 1.) - inter)
                    iou = inter / union
                    for m in xrange(len(iou)):
                        if iou[m] >= 0.08:
                            nonface_flag = 0
                            break
                if nonface_flag == 1:
                    c_img = img[c_bbox[1]:c_bbox[3]+1, c_bbox[0]:c_bbox[2]+1]
                    c_img = cv2.resize(c_img, (24, 24), interpolation=cv2.INTER_AREA)
                    image_write = os.path.join('./non-face', '%06d.jpg' % (nonface_id))
                    cv2.imwrite(image_write, c_img)
                    fid.write('/home/xiaoran/qxr/datasets/cascade_train2/train_img_set/non-face/%06d.jpg' % (nonface_id) + '\n')
                    enough += 1
                    nonface_id += 1
            if enough >= 17:
                break

    print nonface_id
    fid.close()


if __name__ == '__main__':
    datapath = '../../comic/comic_train'
    gtfile = '../../comic/comic_face_train_annot.txt'
    imagefile = '../../comic/comic_face_train_list.txt'
    neglist = './bg.txt'
    create_negsamples(datapath, gtfile, imagefile, neglist)