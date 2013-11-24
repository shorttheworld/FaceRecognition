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
import server
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

def set_snap(child):
   child.send(True)

def configure_main_window():
   '''
   Configures the root window component.
   '''
   root.geometry("1150x400")
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
   fn_entry.grid(row=3, column=4, padx=30)

   ln_label = tk.Label(master=root, text='Last Name', background="#EE8")
   ln_label.grid(row=4, column=3)
   ln_entry = tk.Entry(master=root, width=20)
   ln_entry.grid(row=4, column=4, padx=30)

   pw_label = tk.Label(master=root, text='Username/ Admin Password', background="#EE8")
   pw_label.grid(row=5, column=3)
   pw_entry = tk.Entry(master=root, width=20, show='*')
   pw_entry.grid(row=5, column=4, padx=30)

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

def configure_db_list():
   scrollbar = tk.Scrollbar(master=root, orient="vertical")
   scrollbar.grid(row=3, column=10, rowspan=6, sticky="N"+"S")
   db_list = tk.Listbox(master=root, selectmode="SINGLE", height=16,
                        width=50, yscrollcommand=scrollbar.set)
   db_list.grid(row=3, column=7, rowspan=6, columnspan=3)
   usermode_btn = tk.Button(master=root, text="Users", width=20, command=lambda:switch_mode(0, db_list))
   usermode_btn.grid(row=9, column=7)
   adminmode_btn = tk.Button(master=root, text="Admins", width=20, command=lambda:switch_mode(1, db_list))
   adminmode_btn.grid(row=9, column=8)
   scrollbar.config(command=db_list.yview)
   refresh(0, db_list)
   return db_list

def delete_entry(curSelection, db, db_list):
   try:
      if((curSelection != ()) and (curSelection[0] != '0')):
         cur = str(db_list.get(curSelection))
         if mode == 0:
            (fn, ln, pw) = cur.split()
            db.deleteUser(pw)
            refresh(0, db_list)
         if mode == 1:
            (username, pw) = cur.split()
            db.deleteAdmin(username, pw)
            refresh(1, db_list)
      else:
         tkMessageBox.showwarning(title="Error", message="Please select a valid entry from the list.")
   except(IndexError):
      pass

def switch_mode(flag, db_list):
   global mode
   if flag == 0:
      mode = 0
   if flag == 1:
      mode = 1
   refresh(mode, db_list)

def refresh(mode, db_list):
   if mode == 0:
      user_list = db.getUsers()
      db_list.delete(0, db_list.size())
      db_list.insert(0, "FIRSTNAME    LASTNAME    USERNAME")
      try:
         for (fn, ln, pw) in user_list:
            db_list.insert(db_list.size(), fn + " " + ln + " " + pw)
      except(TypeError):
         pass
   if mode == 1:
      admin_list = db.getAdmins()
      db_list.delete(0, db_list.size())
      db_list.insert(0, "USERNAME    PASSWORD")
      try:
         for (username, pw) in admin_list:
            db_list.insert(db_list.size(), username + " " + pw)
      except(TypeError):
         pass

def configure_buttons(fn_entry, ln_entry, pw_entry, db, queue, child, db_list):
   '''
   Configures the buttons that allow user interactivity.
   '''
   
   adduser_btn = tk.Button(master=root, command=lambda:add_entry(fn_entry, ln_entry, pw_entry, 0, db, db_list), background="Green", width=15, text="Add User")
   adduser_btn.grid(row=6, column=3)

   addadmin_btn = tk.Button(master=root, command=lambda:add_entry(fn_entry, ln_entry, pw_entry, 1, db, db_list), background="#4444FF", width=15, text="Add Admin")
   addadmin_btn.grid(row=7, column=3)

   delete_btn = tk.Button(master=root, command=lambda:delete_entry(db_list.curselection(), db, db_list), background="Orange", width=15, text="Delete Selection")
   delete_btn.grid(row=6, column=4)
   
   quit_btn = tk.Button(master=root, command=lambda:quit(root, p), background="Red", width=15, text="Quit")
   quit_btn.grid(row=7, column=4)

   capture_btn = tk.Button(master=root, command=lambda:set_snap(child), background="#7777FF", text="Take a picture!")
   capture_btn.grid(row=9, column=0)

def auth_admin(root, process, db):
   auth = tk.Toplevel(bg="#EE8")
   auth.title("Admin authentication")
   auth.geometry("500x400")
   auth.protocol('WM_DELETE_WINDOW', lambda:quit(root, p))
   
   msg = tk.Label(auth, bg="#EE8", text="Please enter your credentials and the hostname you wish to connect to.")
   msg.grid(sticky='NE', columnspan=2, pady=20)

   dbu_label = tk.Label(auth, bg="#EE8", text="Database Username")
   dbu_label.grid(row=1, column=0)

   dbu_entry = tk.Entry(auth, width=15)
   dbu_entry.grid(row=2, column=0, pady=20)

   ftpu_label = tk.Label(auth, bg="#EE8", text="FTP Username")
   ftpu_label.grid(row=1, column=1)

   ftpu_entry = tk.Entry(auth, width=15)
   ftpu_entry.grid(row=2, column=1, pady=20)

   dbpw_label = tk.Label(auth, bg="#EE8", text = "Database Password")
   dbpw_label.grid(row=3, column=0)

   dbpw_entry = tk.Entry(auth, width=15)
   dbpw_entry.grid(row=4, column=0, pady=20)

   ftppw_label = tk.Label(auth, bg="#EE8", text = "FTP Password")
   ftppw_label.grid(row=3, column=1)

   ftppw_entry = tk.Entry(auth, width=15)
   ftppw_entry.grid(row=4, column=1, pady=20)

   dbhost_label = tk.Label(auth, bg="#EE8", text="Database Hostname")
   dbhost_label.grid(row=5, column=0)

   dbhost_entry = tk.Entry(auth, width=15)
   dbhost_entry.grid(row=6, column=0, pady=20)

   auth_btn = tk.Button(auth, text="Authenticate", command=lambda:authorize(auth, root, db))
   auth_btn.grid(row=7, column=0)

   cancel_btn = tk.Button(auth, text="Cancel", command=lambda:quit(root, p))
   cancel_btn.grid(row=7, column=1)

def authorize(window, root, db):
   flag = True
   #Need to check here if credentials are valid, then connect to DB/FTP server
   while flag:
      try:
         #db.connect(window.dbu_entry.get(), window.ftpu_entry.get(), window.dbpw_entry.get(), window.ftpu_entry.get(), window.dbhost_entry.get())
         #Also need to save the hostname (open in read mode, take input, then open in write mode and re-save)

         flag = False
      except:
         tkMessageBox.showwarning(title="Error", message="Authentication failed. Please try again.")
   root.deiconify()
   window.destroy()

def add_entry(fn_entry, ln_entry, pw_entry, flag, db, db_list):
   '''
   Checks fields for entry, then makes a sql query with the user input.
   Also allows the user to interface with the database table directly.
   '''
   global mode
   if (flag == 0 and fn_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid first name.")
   elif (flag == 1 and fn_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid admin name.")
   elif (flag == 0 and ln_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid last name.")
   elif (pw_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid password.")
   else:
      if(flag == 0):
         usr = str(fn_entry.get()) + '_' + str(ln_entry.get()) + '_' + str(pw_entry.get())
         path = os.getcwd() + "\\" + usr
         if(os.path.isdir(path) == False):
            tkMessageBox.showwarning(title="Error", message="Please take some pictures to associate with the new user.")
         elif(len(os.listdir(path)) < 12):
            tkMessageBox.showwarning(title="Error", message="Please take more pictures. (12 required, " + str(len(os.listdir(path))) + " current)")
         else:
            #Give text field input, and open each picture in read mode and append to a list
            picList = []
            for pic in os.listdir(path):
               picList.append(cv2.imread(pic))
            db.addUser(fn_entry.get(), ln_entry.get(), pw_entry.get(), picList)
            switch_mode(0, db_list)
      elif(flag == 1):
         db.addAdmin(fn_entry.get(), pw_entry.get())
         switch_mode(1, db_list)

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
   global mode
   mode = 0
    
   configure_main_window()
   (fn_entry, ln_entry, pw_entry) = configure_fields()
   configure_image_window(queue, parent)
   db = server.Server('localhost', 'root', '', 'Chris', 'colliefarms1')
   db_list = configure_db_list()
   configure_buttons(fn_entry, ln_entry, pw_entry, db, queue, child, db_list)
   
   p.start()
   root.withdraw()
   auth_admin(root, p, db)
   root.protocol('WM_DELETE_WINDOW', lambda:quit(root, p))
   root.mainloop()
