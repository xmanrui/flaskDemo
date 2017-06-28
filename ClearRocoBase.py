#!/usr/bin python
# -*- coding: UTF-8 -*-
import os
def get_reco_img(imgDir):

    for name in os.listdir(imgDir):
        imgPath = os.path.join(imgDir, name)

        if os.path.isfile(imgPath):
            continue

        if os.path.isdir(imgPath):

            for f in os.listdir(imgPath):

                if os.path.isfile(os.path.join(imgPath,f)) and f.lower().endswith(('.png', '.jpg')):

                    command = "rm -rf %s" % os.path.join(imgPath,f)
                    if 0 == os.system(command):
                        print "Clear %s ..." % os.path.join(imgPath,f)

get_reco_img('/home/lurx/pds3/static/Recoraw/')
