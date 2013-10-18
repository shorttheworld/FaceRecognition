#!/usr/bin/python

# Hannah's vesion of the gui

import cv2
import numpy as np
from multiprocessing import Process, Queue
from Queue import Empty

from PIL import Image, ImageTk
import Tkinter as tk
import time

import sys, getopt

from video import create_capture

# tkinter GUI functions ---------------------------------------------------------
def update_image(image_label, queue):
   frame = queue.get()
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

# Multiprocessing image processing functions ------------------------------------
def image_capture(queue):
   cascade_fn = "../metadata/haarcascade_frontalface_alt.xml"
   cascade = cv2.CascadeClassifier(cascade_fn)
        
   vidFile = create_capture(0)
   
   curr = 1

   success, frame = vidFile.read() 

   while success != 0:
      try:
         success, frame = vidFile.read() 
         
         frame = frame[frame.shape[1]/2-150:frame.shape[1]/2+200, frame.shape[0]/2-50:frame.shape[0]/2+250]

         '''
         rects = detect(frame, cascade)
         
         if(rects != []):
            if goodOrBad(frame,cascade, curr):
               curr = curr +1
               found = True
               lf.config(bg = "Green")
               lf_text.config(text="Face Detected", bg="Green")
            else:
               lf.config(bg = "Red")
               lf_text.confid(text="Searching for a face...", bg="Red")
         '''
         
        
         queue.put(frame) 
         cv2.waitKey(20)

      except:
         continue


# Database functions ------------------------------------------------------------
def setup_db():
   db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="FacialRecognition") 
   global cur
   cur = db.cursor() 

def get_name(pin):
   cmd = "SELECT first_name, last_name FROM person WHERE pin=" + str(pin)
   cur.execute(cmd)
   person = cur.fetchone()

   print person[0] + " " + person[1]

if __name__ == '__main__':
   queue = Queue()
   root = tk.Tk()

   image_label = tk.Label(master=root)
   image_label.pack()

   p = Process(target=image_capture, args=(queue,))
   p.start()
   
   quit_button = tk.Button(master=root, text='Quit',command=lambda: quit(root,p))
   quit_button.pack()
   
   root.after(0, func=lambda: update_all(root, image_label, queue))
   root.mainloop()