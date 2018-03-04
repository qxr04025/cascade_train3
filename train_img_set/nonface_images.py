#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'qxr'


import cv2
import os
import os.path
import sys
from IPython import embed

def nonface_image(gtfile, neglist):
    nonface_id = 0
    fid = open(neglist, 'w')
    with open(gtfile) as f:
        lines = f.readlines()
        idx = 0
        while idx < len(lines):
            image_name = lines[idx].strip()
            print 'Processing ' + image_name
            image_read = os.path.join('../../comic/comic_train', image_name)
            image = cv2.imread(image_read)
            imw = image.shape[1]
            imh = image.shape[0]

            idx += 1
            num_boxes = int(lines[idx])

            for i in xrange(num_boxes):
                idx += 1
                coor = map(int, lines[idx].split())
                x1 = min(max(coor[0], 0), imw - 1)
                y1 = min(max(coor[1], 0), imh - 1)
                x2 = min(max(x1 + coor[2] - 1, 0), imw - 1)
                y2 = min(max(y1 + coor[3] - 1, 0), imh - 1)
                re_image = image
                for xx in range(x1,x2+1):
                    for yy in range(y1, y2+1):
                        re_image[yy, xx, 0] = 255
                        re_image[yy, xx, 1] = 255
                        re_image[yy, xx, 2] = 255

            image_write = os.path.join('./non-face', '%06d.jpg'%(nonface_id))
            cv2.imwrite(image_write, re_image)
            fid.write('/home/qinxiaoran/program/cascade_train3/train_img_set/non-face/%06d.jpg'%(nonface_id) + '\n')
            nonface_id += 1

            idx += 1

        assert(idx == len(lines))
    fid.close()
    print nonface_id


if __name__ == '__main__':
    gtfile = '../../comic/comic_face_train_annot.txt'
    neglist = './bg.txt'
    nonface_image(gtfile, neglist)