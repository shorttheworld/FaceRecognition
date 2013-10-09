#!/usr/bin/env python

import cv2
import gtk

# local modules
from video import create_capture
from common import clock, draw_str

if __name__ == '__main__':
    video_src = 0 
    cam = create_capture(video_src)
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_default_size(500, 400)
    window.add(gtk.Button("Start"))
    window.show_all()
    
    while True:
        #ret, img = cam.read()
        #cv2.imshow('facedetect', img)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()