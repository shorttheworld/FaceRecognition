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

from FaceRecognizer import *

# tkinter GUI functions ---------------------------------------------------------
def update_video_feed(image_label, frame):
   '''
   Updates the image label containing the video feed.
   '''
   img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(img)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(image_label, queue):
   '''
   Recursively updates the entire GUI after each frame.
   '''
   frame = queue.get()
   update_video_feed(image_label, frame)
   root.after(0, func=lambda: update_all(image_label, queue))

def quit(root, process):
   '''
   Kills the GUI and the related video feed process.
   '''
   process.terminate()
   root.destroy()

# Multiprocessing image processing functions ------------------------------------
def video_feed(queue):
   '''
   Reads from a video capture and puts a frame in the queue.
   '''
   video = create_capture(0)
   success, frame = video.read()

   while success != 0:
      frame = crop_frame(frame)   
      queue.put(frame)
      success, frame = video.read()

def crop_frame(frame):
   '''
   Crops the video frame to a standard size.
   '''
   height = 350
   width = 300
   x_offset = 90
   y_offset = -10

   dim_l = frame.shape[0]/2 - width/2 + x_offset
   dim_r = frame.shape[0]/2 + width/2 + x_offset
   dim_b = frame.shape[1]/2 - height/2 + y_offset
   dim_t = frame.shape[1]/2 + height/2 + y_offset

   frame = frame[dim_b:dim_t, dim_l:dim_r]

   return frame

# Face detection ----------------------------------------------------------------
def start_detection(queue, image_label, lf, lf_label):
   '''
   Runs the detection algorithm and grabs multiple frames for the recognizer to compare.
   '''
   configure_folders()

   cascade_fn = "../metadata/haarcascade_frontalface_alt.xml"
   cascade = cv2.CascadeClassifier(cascade_fn)
   
   max_capture_attempts = 50
   num_pics_required = 30
   configure_folders()
   for i in range (0, max_capture_attempts):
      frame = queue.get()

      update_video_feed(image_label, frame)
      detect_face(frame, cascade)
      update_labels(lf, lf_label, num_pics_required)

      print i

      if (num_pics_captured() == 30):
         break;

def detect_face(frame, cascade):
   '''
   Attempts to detect a face in the video feed.
   '''
   img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   #img = cv2.equalizeHist(gray)

   # detectMultiScale is causing the video to slow down
   rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, 
      minSize=(30, 30), flags =cv2.CASCADE_SCALE_IMAGE) #CV_HAAR_SCALE_IMAGE

   if len(rects) != 0:
      # Can someone clean this line up and verify that I didn't mess it up? It's a bit hacky
      crop_img = img[(rects[0][1]-20):(rects[0][1] + 204), (rects[0][0]-5):(rects[0][0]+179)]

      #Hannah: :D this if statement is required, It checks to see if the image dimensions are correct :D
      if len(crop_img) == 224 and len(crop_img[0]) == 184:
         crop_img = cv2.resize(crop_img,(92,112))
         cv2.imwrite("victim/" + str(num_pics_captured()) + ".pgm" , crop_img)  

def update_labels(lf, lf_label, num_pics_required):
   '''
   Updates the labels to remain current with the face detection.
   '''
   num_pics = num_pics_captured()
   lf_color = lf['bg']

   if (lf_color != 'red' and num_pics == 0):
      lf.config(bg='red')
      lf_label.config(bg='red', text='Searching for face...')
      root.update()
   elif (lf_color != 'yellow' and 0 < num_pics and num_pics < num_pics_required-1):
      lf.config(bg='yellow')
      lf_label.config(bg='yellow', text='Matching face.')
      root.update()
   elif (lf_color != 'green' and num_pics == num_pics_required-1):
      lf.config(bg='green')
      lf_label.config(bg='green', text='Detected: ' + recognize_face())
      root.update()

def recognize_face():
   '''
   Runs the face recognition algorithm on the appropriate frames.
   '''
   # Saman: add face recognizer here
   # Hannah: Done!
   
   recognizer = FaceRecognizer.FaceRecognizer()
   name = recognizer.result()
   #name = ":D"

   return name

def num_pics_captured():
   '''
   Tracks the number of pictures captured for the current subject.
   '''
   fileList = os.listdir(os.getcwd() + '/victim/')
   num_pics = len(fileList)

   return num_pics
      
# Database functions ------------------------------------------------------------
def setup_db():
   '''
   Establishes a connection to the locally hosted database for user authentication.
   '''
   # mysql -u root -p FacialRecognition; root
   mySQL = MySQLdb.connect(host="localhost", user="root", passwd="root", db="FacialRecognition") 
   db = mySQL.cursor() 

def get_name(db, password):
   '''
   Retreives a name from the database corresponding to the password the user entered.
   '''
   if sanitize_input(password):
      cmd = "SELECT first_name, last_name FROM person WHERE password=" + str(password)
      db.execute(cmd)
      person = db.fetchone()

      return person[0] + " " + person[1]

def sanitize_input(input):
   '''
   Makes sure input is not harmful to the database.
   '''
   return True #To be implemented later if necessary

# Configure GUI components ------------------------------------------------------
def configure_main_window():
   '''
   Configures the root window component.
   '''
   root.geometry("700x400")
   root.resizable(width=False, height=False)
   root.configure(background="#FFF")
   root.title("In Yo Face")

def configure_welcome_banner():
   '''
   Configures the welcome banner.
   '''
   welcome_font = tkFont.Font(family='Helvetica', size=12, weight='bold')
   
   welcome_frame = tk.LabelFrame(master=root, relief="ridge", bg='black')
   welcome_frame.grid(row=0, column=1, columnspan=2)
   
   welcome_message = 'Welcome to the In Yo Face Authentication System!'
   welcome_label = tk.Label(master=welcome_frame, text=welcome_message, font=welcome_font)
   welcome_label.grid(row=0, column=1, columnspan=2)

def configure_folders():
   '''
   Creates a fresh victim folder for the current capture.
   '''
   curPath = os.getcwd()
   if(('victim' in os.listdir(curPath)) == True):
      shutil.rmtree('victim')
   os.mkdir('victim')

def configure_labels():
   '''
   Configures the label prompting the user entry.
   '''
   lf = tk.LabelFrame(master=root, bg='red', bd=10, width=30, height=1)
   lf.grid(row=3, column=1)

   lf_label = tk.Label(master=lf, text='Enter a password.', bg='red', width=35)
   lf_label.grid(row=3, column=1)

   return (lf, lf_label)

def configure_image_window(queue):
   '''
   Configures the image window for the video feed.
   '''
   image_label = tk.Label(master=root)
   image_label.grid(row=3, column=0, rowspan=3)

   root.after(0, func=lambda: update_all(image_label, queue))

   return image_label

def configure_buttons(queue, image_label, lf, lf_label):
   '''
   Configures the buttons that allow user interactivity.
   '''
   entry = tk.Entry(master=root, show='*', bg='white', fg='black', takefocus=1, width=30)
   entry.grid(row=4, column=1, sticky="n")
   
   enter_button = tk.Button(master=root, text='Enter', command=lambda: 
      start_detection(queue, image_label, lf, lf_label), bg='green', width=25, height=1)
   enter_button.grid(row=4, column=1)

   quit_button = tk.Button(master=root, text='Quit', command=lambda: quit(root, p), bg='red', width=25, height=1)
   quit_button.grid(row=4, column=1, sticky="s")

   return entry

# Bash commands -----------------------------------------------------------------
def sh(script):
   '''
   Converts a string into a shell script.
   '''
   os.system("bash -c '%s'" % script)

# Main method -------------------------------------------------------------------
if __name__ == '__main__':
   '''
   Main method. Configures all parts of the GUI as well as the video feed process, then calls the main loop.
   '''
   queue = Queue()
   root = tk.Tk()

   p = Process(target=video_feed, args=(queue,))

   #db = setup_db()

   configure_main_window()
   configure_welcome_banner()
   configure_folders()

   lf, lf_label = configure_labels()
   image_label = configure_image_window(queue)
   entry = configure_buttons(queue, image_label, lf, lf_label)
   
   p.start()
   root.mainloop()
