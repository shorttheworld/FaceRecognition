#!/usr/bin/env python

import numpy as np
import cv2

# local modules
from video import create_capture
from common import clock, draw_str
import cv2.cv as cv
from video import create_capture
from goodBad import goodOrBad

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

class Detector:

    def detect(self,img, cascade):
        # rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        rects = cascade.detectMultiScale(img)#, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)

        if len(rects) == 0:
            print "here fuck"
            return []
        print "booooooooooooob"
        return rects

    def detectFace(self):
        print "stuff"
        import sys, getopt
        print help_message

        args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
        try: video_src = video_src[0]
        except: video_src = 0
        args = dict(args)
        # cascade_fn = args.get('--cascade', "haarcascade_frontalface_alt.xml")
        cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        
        cam = create_capture(video_src, fallback='synth:bg=lena.jpg:noise=0.05')
        found = False
        
        while True:
            ret, img = cam.read()
            rects = self.detect(img, cascade)
            vis = img.copy()
            if(rects != [] and found == False):
                print "here"
                if goodOrBad(img,cascade):
                    found = True

            cv2.imshow('facedetect', vis)

            if 0xFF & cv2.waitKey(5) == 27:
                break
        cv2.destroyAllWindows()

d = Detector()
d.detectFace()
