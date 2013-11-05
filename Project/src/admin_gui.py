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
   img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(img)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(image_label, queue):
   frame = queue.get()
   update_video_feed(image_label, frame)
   root.after(0, func=lambda: update_all(image_label, queue))

def video_feed(queue):
   video = create_capture(0)
   success, frame = video.read()

   while success != 0:
      
      frame = crop_frame(frame)   
      queue.put(frame)
      success, frame = video.read()

def crop_frame(frame):
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

def snap_pics(threshold, queue, pw):
    loc = os.getcwd()
    loc = loc.strip("\src")
    loc += "\data"
    print loc
    
    cur=len(os.listdir(loc)) #this will access the file system where the pictures are and find how
    #many have been taken
    print cur
    if(cur<threshold):
        #need help with live feed capture here: basically need to take a photo
        #and store it elsewhere in the file system until we have enough.
        return True
    else:
        return False

def configure_main_window():
    root.geometry("700x400")
    root.resizable(width=False, height=False)
    root.configure(background="#EE8")
    root.title("In Yo Face Admin Tools")

def configure_fields():
    fn_label = tk.Label(master=root, text='First Name', background="#EE8")
    fn_label.grid(row=3, column=3)
    fn_entry = tk.Entry(master=root, width=20)
    fn_entry.grid(row=3, column=4)

    ln_label = tk.Label(master=root, text='Last Name', background="#EE8")
    ln_label.grid(row=4, column=3)
    ln_entry = tk.Entry(master=root, width=20)
    ln_entry.grid(row=4, column=4)

    pw_label = tk.Label(master=root, text='Password', background="#EE8")
    pw_label.grid(row=5, column=3)
    pw_entry = tk.Entry(master=root, width=20, show='*')
    pw_entry.grid(row=5, column=4)

    return (fn_entry, ln_entry, pw_entry)

def configure_image_window(queue):
   image_label = tk.Label(master=root)
   image_label.grid(row=3, column=0, rowspan=5)

   root.after(0, func=lambda: update_all(image_label, queue))

def configure_buttons(fn_entry, ln_entry, pw_entry, db, queue):
    adduser_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 0, db), background="Green", width=15, text="Add User")
    adduser_btn.grid(row=6, column=4)

    addadmin_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 1, db), background="#4444FF", width=15, text="Add Admin")
    addadmin_btn.grid(row=7, column=4)

    delete_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 2, db), background="Orange", width=15, text="Delete User")
    delete_btn.grid(row=6, column=5)
   
    quit_btn = tk.Button(master=root, command=lambda:quit(root, p), background="Red", width=15, text="Quit")
    quit_btn.grid(row=7, column=5)

    capture_btn = tk.Button(master=root, command=lambda:snap_pics(12, queue, pw_entry), background="#7777FF", text="Take a picture!")
    capture_btn.grid(row=9, column=0)
    

def db_interface(fn_entry, ln_entry, pw_entry, flag, db):#Need to add DB as a param
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
   process.terminate()
   root.destroy()

def sanitize_input(entry):
   return True

if __name__== '__main__':
    root = tk.Tk()
    queue = Queue()
    p = Process(target=video_feed, args=(queue,))
    
    configure_main_window()
    (fn_entry, ln_entry, pw_entry) = configure_fields()
    configure_image_window(queue)
    db = DB.DB()
    configure_buttons(fn_entry, ln_entry, pw_entry, db, queue)

    p.start()
    root.mainloop()
