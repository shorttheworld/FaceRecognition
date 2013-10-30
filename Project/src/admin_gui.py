#!/usr/bin/python

import Tkinter as tk
import tkFont
from PIL import Image, ImageTk

import cv2
import numpy as np

from multiprocessing import Process, Queue
from video import create_capture
import time

def update_video_feed(image_label, frame):
   print "update video feed"
   img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(img)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(image_label, queue):
   print "update all"
   frame = queue.get()
   update_video_feed(image_label, frame)
   root.after(0, func=lambda: update_all(image_label, queue))

def video_feed(queue):
   print "Creating Video Feed"
   video = create_capture(0)
   success, frame = video.read()

   while success != 0:
      print "Read unsuccessful"
      success, frame = video.read()
      frame = crop_frame(frame)   
      queue.put(frame) 

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

def snap_pic(threshold):
    cur=0 #this will access the file system where the pictures are and find how
    #many have been taken
    if(cur<threshold):
        #need help with live feed capture here: basically need to take a photo
        #and store it elsewhere in the file system until we have enough.
        return True
    else:
        return False

def configure_main_window():
    root.geometry("800x500")
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
   print "configure image window"
   image_label = tk.Label(master=root)
   image_label.grid(row=3, column=0, rowspan=3)

   root.after(0, func=lambda: update_all(image_label, queue))

   return image_label

def configure_buttons(fn_entry, ln_entry, pw_entry):
    continue_btn = tk.Button(master=root, command=lambda:check_fields(fn_entry, ln_entry, pw_entry), background="Green", width=15, text="Continue")
    continue_btn.grid(row=6, column=4,)

    quit_btn = tk.Button(master=root, command=lambda:quit(root, p), background="Red", width=15, text="Quit")
    quit_btn.grid(row=6, column=5,)

    capture_btn = tk.Button(master=root, command=lambda:snap_pic(12), background="#7777FF", text="Take a picture!")
    capture_btn.grid(row=7, column=0)
    

def check_fields(fn_entry, ln_entry, pw_entry):
    err_label = tk.Label(master=root, bg="#EE8")
    err_label.grid(row=7, column=4)
    if (fn_entry.get() == ''):
        err_label.configure(text="Please enter a valid first name")
        return False
    elif (ln_entry.get() == ''):
        err_label.configure(text="Please enter a valid last name")
        return False
    elif (pw_entry.get() == ''):
        err_label.configure(text="Please enter a valid password")
        return False
    elif (sanitize_input(pw_entry.get) == False):
        err_label.configure(text="Please enter a valid password")
        return False
    else:
        err_label.configure(text='')
        return (fn_entry, ln_entry, pw_entry)

def quit(root, process):
   process.terminate()
   root.destroy()

def sanitize_input(input):
   return True

if __name__== '__main__':
    root = tk.Tk()
    queue = Queue()

    p = Process(target=video_feed, args=(queue,))
    
    configure_main_window()
    (fn_entry, ln_entry, pw_entry) = configure_fields()
    configure_image_window(queue)
    configure_buttons(fn_entry, ln_entry, pw_entry)

    p.start()
    root.mainloop()
