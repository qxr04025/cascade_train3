#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'qxr'

import os
import os.path

def create_bg(filename):
    fid = open('/home/xiaoran/桌面/cascade_train/bg.txt', 'w')
    with open(filename) as f:
        lines = f.readlines()
        idx = 0
        while idx < len(lines):
            image_name = lines[idx].strip()
            image_name = os.path.join('/home/qxr/program/cascade_train/train_img_set/non-face', image_name)
            fid.write(image_name + '\n')
            idx += 1
        assert (idx == len(lines))
    fid.close()

if __name__ == '__main__':
    filename = '/home/xiaoran/桌面/cascade_train/neglist.txt'
    create_bg(filename)