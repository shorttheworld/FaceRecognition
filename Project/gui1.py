#!/usr/bin/env python

import cv2
#import gtk

# local modules
from video import create_capture
from common import clock, draw_str

class Camera:
	def __init__(self):
		video_src = 0
		self.cam = create_capture(video_src)

	def on_mouse(self, event, x, y, flag, param):
		if (event == cv2.CV2_EVENT_LBUTTONDOWN):
			print 'hi'

	def main(self):
	    cv2.namedWindow("windowwww");
	    
	    while True:
	        ret, img = self.cam.read()
	        cv2.imshow('Face Detect', img)
	    	cv2.setMouseCallback("windowwww", self.on_mouse, 'HI')

	        if 0xFF & cv2.waitKey(5) == 27:
	            break
	    cv2.destroyAllWindows()

if __name__ == '__main__':
    camera = Camera()
    camera.main()