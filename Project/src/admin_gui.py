#!/usr/bin/python

import Tkinter as tk
import tkMessageBox
import tkFont
from PIL import Image, ImageTk

import cv2
import numpy as np
from Queue import Empty

from multiprocessing import Process, Queue, Pipe
from video import create_capture

import time
import DB
import os
import socket

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

def update_all(image_label, queue, parent):
   '''
   Recursively updates the entire GUI after each frame.
   '''
   frame = queue.get()
   update_video_feed(image_label, frame)
   try:
      (fn, ln, pw) = read_fields()
      if(parent.poll()):
         parent.recv()
         snap_pics(frame, fn, ln, pw)
      root.after(0, func=lambda: update_all(image_label, queue, parent))
   except Exception:
      pass

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
   usr = str(fn) + '_' + str(ln) + '_' + str(pw)
   path = os.getcwd() + "\\" + usr
   if(os.path.isdir(path) == False):
      os.mkdir(path)

   crop_img = crop_frame(frame)
   cur=len(os.listdir(path)) #this will access the file system where the pictures are and find how
   #many have been taken
   if(cur<12):
      #Store photo in the folder
      cv2.imwrite(path + "\\" + str(cur) + ".pgm", crop_img)
   else:
      #Call Solace's function
      #Delete the folder
      return False

def set_snap(child):
   child.send(True)

def configure_main_window():
   '''
   Configures the root window component.
   '''
   root.geometry("1300x400")
   root.resizable(width=False, height=False)
   root.configure(background="#EE8")
   root.title("In Yo Face Admin Tools")

def configure_fields():
   '''
   Configures the fields for user entry.
   '''
   fn_label = tk.Label(master=root, text='First Name/Admin Name', background="#EE8")
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

def read_fields():
   return (fn_entry.get(), ln_entry.get(), pw_entry.get())

def configure_image_window(queue, parent):
   '''
   Configures the image window for the video feed.
   '''
   image_label = tk.Label(master=root)
   image_label.grid(row=3, column=0, rowspan=5,)

   root.after(0, func=lambda: update_all(image_label, queue, parent))

def configure_db_list(db):
   scrollbar = tk.Scrollbar(master=root, orient="vertical")
   scrollbar.grid(row=3, column=9, rowspan=7, sticky="N"+"S")
   db_list = tk.Listbox(master=root, selectmode="SINGLE", height=18,
                        width=50, yscrollcommand=scrollbar.set)
   db_list.grid(row=3, column=6, rowspan=7, columnspan=3)
   db_list.insert(0, "FIRST NAME    LAST NAME    PASSWORD")
   scrollbar.config(command=db_list.yview)
   for num in range(50):
      db_list.insert(db_list.size(), num)
   #Need to call a function in the DB class here to populate the table
   return db_list

def configure_buttons(fn_entry, ln_entry, pw_entry, db, queue, child, db_list):
   '''
   Configures the buttons that allow user interactivity.
   '''
   adduser_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 0, db), background="Green", width=15, text="Add User")
   adduser_btn.grid(row=6, column=3)

   addadmin_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 1, db), background="#4444FF", width=15, text="Add Admin")
   addadmin_btn.grid(row=7, column=3)

   delete_btn = tk.Button(master=root, command=lambda:db_interface(fn_entry, ln_entry, pw_entry, 2, db), background="Orange", width=15, text="Delete User")
   delete_btn.grid(row=6, column=4)
   
   quit_btn = tk.Button(master=root, command=lambda:quit(root, p), background="Red", width=15, text="Quit")
   quit_btn.grid(row=7, column=4)

   capture_btn = tk.Button(master=root, command=lambda:set_snap(child), background="#7777FF", text="Take a picture!")
   capture_btn.grid(row=9, column=0)

def auth_admin(root, process):
   auth = tk.Toplevel(bg="#EE8")
   auth.title("Admin authentication")
   auth.geometry("400x300")
   auth.protocol('WM_DELETE_WINDOW', lambda:quit(root, p))
   
   msg = tk.Message(auth, bg="#EE8", text="Please enter your credentials and the hostname you wish to connect to.")
   msg.pack()

   auth_label = tk.Label(auth, bg="#EE8", text="Username")
   auth_label.pack()

   auth_entry = tk.Entry(auth, width=15)
   auth_entry.pack()

   pw_label = tk.Label(auth, bg="#EE8", text ="Password")
   pw_label.pack()

   pw_entry = tk.Entry(auth, width=15)
   pw_entry.pack()

   host_label = tk.Label(auth, bg="#EE8", text="Hostname")
   host_label.pack()

   host_entry = tk.Entry(auth, width=15)
   host_entry.pack()

   auth_btn = tk.Button(auth, text="Authenticate", command=lambda:authorize(auth, root))
   auth_btn.pack()

   cancel_btn = tk.Button(auth, text="Cancel", command=lambda:quit(root, p))
   cancel_btn.pack()

def authorize(window, root):
   #Need to check here if credentials are valid

   #Also need to save the hostname (open in read mode, take input, then open in write mode and re-save)
   root.deiconify()
   window.destroy()

def db_interface(fn_entry, ln_entry, pw_entry, flag, db, db_list):
   '''
   Checks fields for entry, then makes a sql query with the user input.
   Also allows the user to interface with the database table directly.
   '''
   
   if (flag != 1 and fn_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid first name.")
   elif (flag == 1 and fn_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid admin name")
   elif (flag != 1 and ln_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid last name")
   elif (flag != 2 and pw_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid password.")
   else:
      if(flag == 0):
         #Need FN, LN, PW, picList(open each picture in read mode and append to a list)
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

if __name__== '__main__':
   '''
   Main method. Configures all parts of the GUI as well as the video feed process, then calls the main loop.
   '''
   root = tk.Tk()
   queue = Queue()
   (parent, child) = Pipe()
   p = Process(target=video_feed, args=(queue,))
    
   configure_main_window()
   (fn_entry, ln_entry, pw_entry) = configure_fields()
   configure_image_window(queue, parent)
   db = DB.DB()
   db_list = configure_db_list(db)
   configure_buttons(fn_entry, ln_entry, pw_entry, db, queue, child, db_list)
   
   p.start()
   root.withdraw()
   auth_admin(root, p)
   root.protocol('WM_DELETE_WINDOW', lambda:quit(root, p))
   root.mainloop()
