#!/usr/bin/python

import Tkinter as tk
import tkFont
from PIL import Image, ImageTk

import cv2
import numpy as np
from Queue import Empty

from multiprocessing import Process, Queue
from video import create_capture
import time
import DB
import os

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
   (fn, ln, pw) = read_fields()
   if(snap == True):
      snap_pics(frame, fn, ln, pw)
      snap = False;
   root.after(0, func=lambda: update_all(image_label, queue))

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
   x_offset = 100
   y_offset = -10

   dim_l = frame.shape[0]/2 - width/2 + x_offset
   dim_r = frame.shape[0]/2 + width/2 + x_offset
   dim_b = frame.shape[1]/2 - height/2 + y_offset
   dim_t = frame.shape[1]/2 + height/2 + y_offset

   frame = frame[dim_b:dim_t, dim_l:dim_r]

   return frame

def snap_pics(frame, fn, ln, pw):
   '''
   Takes a picture from the video feed and stores it in the filesystem.
   '''
   loc = os.getcwd()
   loc = loc.strip('\\src')
   loc = loc + '\\data\\'
   loc = loc + str(fn) + '_' + str(ln) + '_' + str(pw)
   print loc

   frame = crop_frame(frame) 
   cur=len(os.listdir(loc)) #this will access the file system where the pictures are and find how
   #many have been taken
   print cur
   if(cur<threshold):
      #need help with live feed capture here: basically need to take a photo
      #and store it elsewhere in the file system until we have enough.
      return True
   else:
      return False

def set_snap(TF):
   snap = bool(TF)

def configure_main_window():
   '''
   Configures the root window component.
   '''
   root.geometry("700x400")
   root.resizable(width=False, height=False)
   root.configure(background="#EE8")
   root.title("In Yo Face Admin Tools")

def configure_fields():
   '''
   Configures the fields for user entry.
   '''
   fn_label = tk.Label(master=root, text='First Name', background="#EE8")
   fn_label.grid(row=3, column=3)
   global fn_entry
   fn_entry = tk.Entry(master=root, width=20)
   fn_entry.grid(row=3, column=4)

   ln_label = tk.Label(master=root, text='Last Name', background="#EE8")
   ln_label.grid(row=4, column=3)
   global ln_entry
   ln_entry = tk.Entry(master=root, width=20)
   ln_entry.grid(row=4, column=4)

   pw_label = tk.Label(master=root, text='Password', background="#EE8")
   pw_label.grid(row=5, column=3)
   global pw_entry
   pw_entry = tk.Entry(master=root, width=20, show='*')
   pw_entry.grid(row=5, column=4)

   return (fn_entry, ln_entry, pw_entry)

def read_fields():
   return (fn_entry.get(), ln_entry.get(), pw_entry.get())

def configure_image_window(queue):
   '''
   Configures the image window for the video feed.
   '''
   image_label = tk.Label(master=root)
   image_label.grid(row=3, column=0, rowspan=5)

   capture_btn = tk.Button(master=root, command=lambda:set_snap(True), background="#7777FF", text="Take a picture!")
   capture_btn.grid(row=9, column=0)

   root.after(0, func=lambda: update_all(image_label, queue))

def configure_buttons(fn_entry, ln_entry, pw_entry, db, queue):
   '''
   Configures the buttons that allow user interactivity.
   '''
   adduser_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 0, db), background="Green", width=15, text="Add User")
   adduser_btn.grid(row=6, column=4)

   addadmin_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 1, db), background="#4444FF", width=15, text="Add Admin")
   addadmin_btn.grid(row=7, column=4)

   delete_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 2, db), background="Orange", width=15, text="Delete User")
   delete_btn.grid(row=6, column=5)
   
   quit_btn = tk.Button(master=root, command=lambda:quit(root, p), background="Red", width=15, text="Quit")
   quit_btn.grid(row=7, column=5)

def db_interface(fn_entry, ln_entry, pw_entry, flag, db):
   '''
   Checks fields for entry, then makes a sql query with the user input.
   '''
   err_label = tk.Message(master=root, bg="#EE8")
   err_label.grid(row=4, column=5)
   if (fn_entry.get() == '' or sanitize_input(fn_entry.get) == False):
      err_label.configure(text="Please enter a valid first name")
      return False
   elif (ln_entry.get() == '' or sanitize_input(ln_entry.get) == False):
      err_label.configure(text="Please enter a valid last name")
      return False
   elif (pw_entry.get() == '' or sanitize_input(pw_entry.get) == False):
      err_label.configure(text="Please enter a valid password")
      return False
   else:
      err_label.grid_remove()#Need to figure out how to delete message better
      if(flag == 0):
         db.addUser(fn_entry.get(), ln_entry.get(), pw_entry.get())
      elif(flag == 1):
         db.addAdmin(fn_entry.get(), ln_entry.get(), pw_entry.get())
      elif(flag == 2):
         db.deleteUser(pw_entry.get())

def quit(root, process):
   '''
   Kills the GUI and the related video feed process.
   '''
   process.terminate()
   root.destroy()

def sanitize_input(entry):
   '''
   Makes sure input is not harmful to the database.
   '''
   return True

if __name__== '__main__':
   '''
   Main method. Configures all parts of the GUI as well as the video feed process, then calls the main loop.
   '''
   root = tk.Tk()
   queue = Queue()
   p = Process(target=video_feed, args=(queue,))
   snap = False
    
   configure_main_window()
   (fn_entry, ln_entry, pw_entry) = configure_fields()
   configure_image_window(queue)
   db = DB.DB()
   configure_buttons(fn_entry, ln_entry, pw_entry, db, queue)

   p.start()
   root.mainloop()
