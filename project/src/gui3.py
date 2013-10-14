#!/usr/bin/python

# local modules
from video import create_capture
from common import clock, draw_str
import cv2.cv as cv
from video import create_capture
from goodBad import goodOrBad

import numpy as np
from multiprocessing import Process, Queue
from Queue import Empty
import cv2
from PIL import Image, ImageTk
import time
import Tkinter as tk

#tkinter GUI functions----------------------------------------------------------
def update_image(image_label, queue):
   frame = queue.get()
   # print type(frame)
   im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(im)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(root, image_label, queue):
   update_image(image_label, queue)
   root.after(0, func=lambda: update_all(root, image_label, queue))

def quit(root, process):
   process.terminate()
   root.destroy()

#multiprocessing image processing functions-------------------------------------
def image_capture(queue):
   import sys, getopt

   args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
   try: video_src = video_src[0]
   except: video_src = 0
   args = dict(args)
   cascade_fn = args.get('--cascade', "../metadata/haarcascade_frontalface_alt.xml")
   cascade = cv2.CascadeClassifier(cascade_fn)
        
   vidFile = create_capture(video_src, fallback='synth:bg=lena.jpg:noise=0.05')
   
   curr = 1

   while True:

      try:
         flag, frame = vidFile.read() # what does flag mean?
         frame = frame[frame.shape[1]/2-150:frame.shape[1]/2+200, frame.shape[0]/2-50:frame.shape[0]/2+250]

         rects = detect(frame, cascade)
         
         if(rects != []):
            if goodOrBad(frame,cascade, curr):
               curr = curr +1
               found = True
         
         
         if flag==0:
            break
         queue.put(frame) 	# why is this loading frames onto the queue? because the thread might not
         					# be able to display frames quickly enough?
         
      except:
         continue

def enter_text(entry):
	pin = entry.get()
	print pin

if __name__ == '__main__':
   root = tk.Tk()

   image_label = tk.Label(master=root)# label for the video frame
   image_label.pack()

   #start image capture process
   queue = Queue()
   p = Process(target=image_capture, args=(queue,)) # why is queue passed in as a parameter like this?
   p.start()
   
   quit_button = tk.Button(master=root, text='Quit', command=lambda: quit(root,p)) # what is lambda?
   quit_button.pack()

   entry = tk.Entry(master=root, show='*')
   entry.pack()

   enter_button = tk.Button(master=root, text='Enter', command=lambda: enter_text(entry))
   enter_button.pack()
   
   # setup the update callback
   root.after(0, func=lambda: update_all(root, image_label, queue)) # what is "after"?
   root.mainloop()

#----------------------------------- Saman's stuff------------
def detect(img, cascade):
   rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
   if len(rects) == 0:
      return []
   return rects   