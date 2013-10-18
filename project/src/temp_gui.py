#!/usr/bin/python

# Hannah's vesion of the gui

import cv2
import numpy as np

from multiprocessing import Process, Queue
from Queue import Empty

from PIL import Image, ImageTk
import Tkinter as tk
import tkFont

from video import create_capture
import sys, getopt

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

   video = create_capture(0)

   success, frame = video.read()
   dim_b, dim_t, dim_l, dim_r = slice_frame(frame)
   
   count = 1
   while success != 0:
      success, frame = video.read()
      frame = frame[dim_b:dim_t, dim_l:dim_r]

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.equalizeHist(gray)

      if count < 25:
         rects = detect(gray, cascade, count)
   
         if rects != []:
            count = count + 1
            #face_detected()

      queue.put(frame) 

def slice_frame(frame):
   height = 350
   width = 300

   x_offset = 100
   y_offset = -10

   dim_l = frame.shape[0]/2 - width/2 + x_offset
   dim_r = frame.shape[0]/2 + width/2 + x_offset

   dim_b = frame.shape[1]/2 - height/2 + y_offset
   dim_t = frame.shape[1]/2 + height/2 + y_offset

   return (dim_b, dim_t, dim_l, dim_r)

def detect(img, cascade, count):
   rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, 
      minSize=(30, 30), flags =cv2.CASCADE_SCALE_IMAGE) #CV_HAAR_SCALE_IMAGE

   if len(rects) == 0: 
      rects = []
   else:
      crop_img = img[(rects[0][1]-20):(rects[0][1] + 204), (rects[0][0]-5):(rects[0][0]+179)]
    
      if len(crop_img) == 224 and len(crop_img[0]) == 184:
         newX, newY = crop_img.shape[1]/2, crop_img.shape[0]/2
         crop_img = cv2.resize(crop_img,(newX,newY))
         cv2.imwrite("victim/"+str(count)+".jpg" , crop_img)

   return rects   

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

# Configure GUI components ------------------------------------------------------
def configure_main_window(root):
   root.geometry("800x500")
   root.resizable(width=False, height=False)
   root.configure(background="#EE8")
   root.grid()
   root.title("In Yo Face")

def configure_welcome_banner(root):
   welcome_font = tkFont.Font(family='Helvetica', size=12, weight='bold')
   
   welcome_frame = tk.LabelFrame(master=root, relief="ridge", bg="Black")
   welcome_frame.grid(row=1, column=5, rowspan=3, columnspan=2)
   welcome_frame.pack()
   
   welcome_message = 'Welcome to the In Yo Face Authentication System!'
   welcome_label = tk.Label(master=welcome_frame, text=welcome_message, font=welcome_font)
   welcome_label.pack()

def configure_image_window(root):
   image_label = tk.Label(master=root)
   image_label.grid(row=1, column=1, rowspan=6, columnspan=3)
   image_label.pack()

   return image_label

def face_detected():
   #print 'here'
   #lf.config(bg = "Green")
   print 'here'
   lf_label.config(text="Face Detected", bg="Green")
   print 'here'

# Main method -------------------------------------------------------------------
if __name__ == '__main__':
   queue = Queue()
   root = tk.Tk()

   configure_main_window(root)
   configure_welcome_banner(root)

   image_label = configure_image_window(root)
   
   global lf
   lf = tk.LabelFrame(master=root, bg="Red", bd=10, width=30, height=1)
   lf.grid(row=7, column=1)
   lf.pack()

   color = tk.StringVar()
   color.set('red')

   global lf_labels
   lf_label = tk.Label(master=root, text='Searching for a face...', bg=color.get(), width=35)
   lf_label.pack()

   p = Process(target=image_capture, args=(queue,))
   p.start()
   
   quit_button = tk.Button(master=root, text='Quit',command=lambda: quit(root,p))
   quit_button.pack()
   
   root.after(0, func=lambda: update_all(root, image_label, queue))
   root.mainloop()