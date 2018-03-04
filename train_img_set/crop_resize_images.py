#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'qxr'

import cv2
import os
import os.path
import sys

def crop_resize(gtfile, poslist):
    face_id = 0
    fid = open(poslist, 'w')
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
                crop_image = image[y1:y2+1, x1:x2+1]
                resize_image = cv2.resize(crop_image, (24, 24), interpolation = cv2.INTER_AREA)
                image_write = os.path.join('./face', '%06d.jpg'%(face_id))
                cv2.imwrite(image_write, resize_image)
                fid.write('face/%06d.jpg 1 0 0 24 24'%(face_id) + '\n')
                face_id += 1

            idx += 1

        assert(idx == len(lines))
    fid.close()
    print face_id


if __name__ == '__main__':
    gtfile = '../../comic/comic_face_train_annot.txt'
    poslist = './info.dat'
    crop_resize(gtfile, poslist)