#!/usr/bin/python

# local modules
from video import create_capture
from common import clock, draw_str
#import cv2.cv as cv
from video import create_capture
from goodBad import goodOrBad

import numpy as np
from multiprocessing import Process, Queue
from Queue import Empty
import cv2
from PIL import Image, ImageTk
import time
import Tkinter as tk
import tkFont

import MySQLdb

#tkinter GUI functions----------------------------------------------------------
def update_image(image_label, queue):
   '''
   Updates the image label containing the video feed.
   '''
   frame = queue.get()
   # print type(frame)
   im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(im)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(root, image_label, queue):
   '''
   Recursively updates the entire GUI after each frame.
   '''
   update_image(image_label, queue)
   root.after(0, func=lambda: update_all(root, image_label, queue))

def quit(root, process):
   '''
   Kills the GUI and the related video feed process.
   '''
   process.terminate()
   root.destroy()

#multiprocessing image processing functions-------------------------------------
def image_capture(queue):
   '''
   Attempts to detect a face in the video feed, and adds a frame to the queue.
   '''
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
         # Flag just tells you if it was able to successfully capture the image or not
         frame = frame[frame.shape[1]/2-150:frame.shape[1]/2+200, frame.shape[0]/2-50:frame.shape[0]/2+250]

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
         
         
         if flag==0:
            break
         queue.put(frame) 	# why is this loading frames onto the queue? because the thread might not
         					# be able to display frames quickly enough?
         #This is a producer/consumer type of problem. The queue is thread safe, one process
         # puts things on the queue and another process removes things from ther queue.
         
      except:
         continue

def setup_db():
   '''
   Establishes a connection to the locally hosted database for user authentication.
   '''
   db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="FacialRecognition") 
   global cur
   cur = db.cursor() 

def get_name(pin):
   '''
   Retreives a name from the database corresponding to the password the user entered.
   '''
   cmd = "SELECT first_name, last_name FROM person WHERE pin=" + str(pin)
   cur.execute(cmd)
   person = cur.fetchone()

   print person[0] + " " + person[1]

if __name__ == '__main__':
   '''
   Main method. 
   '''
   root = tk.Tk()
   root.geometry("800x500")
   root.resizable(width=False, height=False)
   root.configure(background="#EE8")
   root.grid()
   root.title("In Yo Face")
   print root.grid_size()

   welcome_font = tkFont.Font(family='Helvetica', size=12, weight='bold')
   
   welcome_frame = tk.LabelFrame(master=root, relief="ridge", bg="Black")
   welcome_frame.grid(row=1, column=5, rowspan=3, columnspan=2)
   
   welcome_label = tk.Label(master=welcome_frame, text='Welcome to the In Yo Face Authentication System!', font=welcome_font)
   welcome_label.pack()
   
   image_label = tk.Label(master=root)# label for the video frame
   image_label.grid(row=1, column=1, rowspan=6, columnspan=3)

   
   global lf
   lf = tk.LabelFrame(master=root, bg="Red", relief="raised", bd=10, width=30, height=1)
   lf.grid(row=7, column=1)
   
   global lf_label
   lf_text = tk.Label(master=lf, text='Searching for a face...', bg="Red", width=35)
   lf_text.pack()
   
   #start image capture process
   queue = Queue()
   p = Process(target=image_capture, args=(queue,)) # why is queue passed in as a parameter like this?
   #Each process takes in the function it's supposed to do and the data structure associated
   # with it. We are passing a queue here so this process can  capture images and put them in the queue
   p.start()

   entry = tk.Entry(master=root, show='*', bg="White", fg="Black", takefocus=1, width=30)
   entry.grid(row=7, column=5)
   
   enter_button = tk.Button(master=root, text='Enter', command=lambda: get_name(pin), bg="green", width=25, height=1)
   enter_button.grid(row=8, column=5)

   quit_button = tk.Button(master=root, text='Quit', command=lambda: quit(root,p), bg="red", width=25, height=1) # what is lambda?
   # Lambda is similar to writing a quick function without having to type def keyword. In this case
   # you have a lambda because the function quit() takes parameters, so we want to pass in the function
   # reference and not the evaluated value
   quit_button.grid(row=9, column=5)
   
   '''
   infoFrame = tk.Frame(master=root, padx=0, pady=0, height='100p', width='100p', bg="Red")
   infoFrame.pack(anchor='e')
   '''
   
   testLabel1 = tk.Label(master=root, text='Room for some user info here.', bg="#EE8")
   testLabel1.grid(row=4, column=5)

   testLabel2 = tk.Message(master=root, text='Messages could work too for stuff that\'s long enough to justify multiple lines.', bg="#EE8")
   #testLabel2.pack(anchor='ne')
   testLabel2.grid(row=5, column=5)
   
   setup_db()

   # setup the update callback
   root.after(0, func=lambda: update_all(root, image_label, queue)) # what is "after"?
   # After means after 0 milliseconds, call some function, in this case update_all. This
   # will only be called once, which is why inside the update_all function there are recursive
   # calls to keep the thread updating the images.
   root.mainloop()

#----------------------------------- Saman's stuff------------
def detect(img, cascade):
   rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
   if len(rects) == 0:
      return []
   return rects   
