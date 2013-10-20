#!/usr/bin/python

# Hannah's vesion of the gui

import os
import shutil

import cv2
import numpy as np

from multiprocessing import Process, Queue
from Queue import Empty

from PIL import Image, ImageTk
import Tkinter as tk
import tkFont

from video import create_capture
import sys, getopt

import FaceRecognizer

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
def video_feed(queue):
   video = create_capture(0)

   success, frame = video.read()
   dim_b, dim_t, dim_l, dim_r = slice_frame(frame)
   
   while success != 0:
      success, frame = video.read()
      frame = frame[dim_b:dim_t, dim_l:dim_r]
      
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

# Face detection ----------------------------------------------------------------
def start_detection(queue, lf, lf_label):
   configure_folders()

   cascade_fn = "../metadata/haarcascade_frontalface_alt.xml"
   cascade = cv2.CascadeClassifier(cascade_fn)
   
   fileList = os.listdir(os.getcwd() + '/victim/')
   num_pics = len(fileList)

   while (num_pics < 50):
      frame = queue.get()

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.equalizeHist(gray)

      rects = detect_face(gray, cascade, num_pics)

      detected_face(lf, lf_label, num_pics)

      fileList = os.listdir(os.getcwd() + '/victim/')
      num_pics = len(fileList)

def detect_face(img, cascade, count):
   rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, 
      minSize=(30, 30), flags =cv2.CASCADE_SCALE_IMAGE) #CV_HAAR_SCALE_IMAGE

   if len(rects) == 0: 
      rects = []
   else:
      #what is this??
      crop_img = img[(rects[0][1]-20):(rects[0][1] + 204), (rects[0][0]-5):(rects[0][0]+179)]
      crop_img = cv2.resize(crop_img,(92,112))
      
      cv2.imwrite("victim/" + str(count) + ".pgm" , crop_img)

   return rects   

def detected_face(lf, lf_label, num_pics):
   color = lf['bg']

   if (color != 'red' and num_pics == 0):
      lf.config(bg="red")
      lf_label.config(bg="red", text='Searching for face...')
   elif (color != 'yellow' and 0 < num_pics and num_pics < 49):
      lf.config(bg="yellow")
      lf_label.config(bg="yellow", text='Matching face.')
   elif (color != 'green' and num_pics == 49):
      #name = db.get_name(db, '12345')
      name = recognize_face()
      lf.config(bg="green")
      lf_label.config(bg="green", text='Detected: ' + name)
      # call Saman

def recognize_face():
   recognizer = FaceRecognizer.FaceRecognizer()
   name = recognizer.result()
   return name
      
# Database functions ------------------------------------------------------------
def setup_db():
   # mysql -u root -p FacialRecognition; root
   mySQL = MySQLdb.connect(host="localhost", user="root", passwd="root", db="FacialRecognition") 
   db = mySQL.cursor() 

def get_name(db, password):
   if sanitize_input(password):
      cmd = "SELECT first_name, last_name FROM person WHERE password=" + str(password)
      db.execute(cmd)
      person = db.fetchone()

      return person[0] + " " + person[1]

def sanitize_input(input):
   return True
   # Make sure input is not harmful to DB

# Configure GUI components ------------------------------------------------------
def configure_main_window(root):
   root.geometry("800x500")
   root.resizable(width=False, height=False)
   root.configure(background="#EE8")
   root.title("In Yo Face")

def configure_welcome_banner(root):
   welcome_font = tkFont.Font(family='Helvetica', size=12, weight='bold')
   
   welcome_frame = tk.LabelFrame(master=root, relief="ridge", bg="black")
   welcome_frame.grid(row=0, column=1, columnspan=2)
   
   welcome_message = 'Welcome to the In Yo Face Authentication System!'
   welcome_label = tk.Label(master=welcome_frame, text=welcome_message, font=welcome_font)
   welcome_label.grid(row=0, column=1, columnspan=2)

def configure_labels(root):
   global lf
   lf = tk.LabelFrame(master=root, bg="red", bd=10, width=30, height=1)
   lf.grid(row=3, column=1)

   global lf_label
   lf_label = tk.Label(master=lf, text='Enter a password.', bg="red", width=35)
   lf_label.grid(row=3, column=1)

def configure_image_window(root, queue):
   image_label = tk.Label(master=root)
   image_label.grid(row=3, column=0, rowspan=3)

   root.after(0, func=lambda: update_all(root, image_label, queue))

def configure_buttons(root, p, queue):
   global entry
   entry = tk.Entry(master=root, show='*', bg="white", fg="black", takefocus=1, width=30)
   entry.grid(row=4, column=1, sticky="n")
   
   enter_button = tk.Button(master=root, text='Enter', command=lambda: start_detection(queue, lf, lf_label), 
      bg="green", width=25, height=1)
   enter_button.grid(row=4, column=1)

   quit_button = tk.Button(master=root, text='Quit', command=lambda: quit(root, p), bg="red", width=25, height=1)
   quit_button.grid(row=4, column=1, sticky="s")

def configure_folders():
   curPath = os.getcwd()
   if(('victim' in os.listdir(curPath)) == True):
      shutil.rmtree('victim')
   os.mkdir('victim')

# Bash commands -----------------------------------------------------------------
def sh(script):
   os.system("bash -c '%s'" % script)

# Main method -------------------------------------------------------------------
if __name__ == '__main__':
   queue = Queue()
   root = tk.Tk()

   p = Process(target=video_feed, args=(queue,))

   #db = setup_db()

   configure_main_window(root)
   configure_welcome_banner(root)
   configure_labels(root)
   configure_buttons(root, p, queue)
   configure_image_window(root, queue)
   configure_folders()
   
   p.start()
   root.mainloop()
