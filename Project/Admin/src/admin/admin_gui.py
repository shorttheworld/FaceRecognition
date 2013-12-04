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
import learnerGenerator
import FTPLearner

import time
import server
import os
import socket
import shutil
import hashlib

#Video Feed-related Functions
#------------------------------------------------------

def video_feed(queue):
   '''
   Reads from a video capture and puts a frame in the queue.
   '''
   video = create_capture(0)
   success, frame = video.read()

   #Continuously grab frames and put them in the queue
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
      #Check for a frame capture request from the pipe
      if(parent.poll()):
         parent.recv()
         snap_pics(frame, pw)
      root.after(0, func=lambda: update_all(image_label, queue, parent))
   except Exception:
      pass

def snap_pics(frame, pw):
   '''
   Takes a picture from the video feed and stores it in the filesystem.
   '''
   if '' in read_fields():
      tkMessageBox.showwarning(title="Error", message="Please enter valid user information before taking photos")
   else:
      path = os.getcwd() + "/../../data/" + pw + "/"
      #Create a folder if the user has no other pictures
      if(os.path.isdir(path) == False):
         os.mkdir(path)
      #Warn the user if the name is already taken
      elif((os.path.isdir(path) == True) and (len(os.listdir(path)) == 12)):
         tkMessageBox.showwarning(title="Error", message="That username is already in use.")

      crop_img = crop_frame(frame)
      cur=len(os.listdir(path)) #this will access the file system where the pictures
      #are and find out how many have been taken
      if(cur<12):
         #Store photo in the folder
         cv2.imwrite(path + str(cur) + ".pgm", crop_img)


#Authorization functions
#------------------------------------------------------
def auth_admin(root, process, db):
   '''
   Allows the admin to log in with proper credentials.
   '''
   #Resize window and lock it to preserve component positions
   auth = tk.Toplevel(bg="#EE8")
   auth.title("Admin authentication")
   auth.geometry("500x425")
   auth.resizable(width=False, height=False)
   auth.protocol('WM_DELETE_WINDOW', lambda:quit(root, p, db))
   
   msg = tk.Label(auth, bg="#EE8", text="Please enter your credentials.")
   msg.pack(pady=10)

   #Username
   adminun_label = tk.Label(auth, bg="#EE8", text="Username")
   adminun_label.pack(pady=10)
   adminun_entry = tk.Entry(auth, width=15)
   adminun_entry.pack(pady=10)

   #Password
   adminpw_label = tk.Label(auth, bg="#EE8", text = "Password")
   adminpw_label.pack(pady=10)
   adminpw_entry = tk.Entry(auth, width=15, show="*")
   adminpw_entry.pack(pady=10)

   try:
      last = open(os.getcwd() + "/../../metadata/lastlogin.txt", "r")
      last_str = last.read().split()
   except:
      last_str = ''

   if(len(last_str) == 2):
      adminun_entry.insert(0, last_str[0])
      adminpw_entry.insert(0, last_str[1])
   else:
      pass
      

   auth_btn = tk.Button(auth, text="Authenticate", command=lambda:authorize(auth, root, db, adminun_entry.get(), adminpw_entry.get()))
   auth_btn.pack(pady=10)

   cancel_btn = tk.Button(auth, text="Cancel", command=lambda:quit(root, p, db))
   cancel_btn.pack(pady=10)

def authorize(window, root, db, username, pw):
   '''
   Checks authorization input against the database.
   '''
   try:
      admin = db.getAdmin(username)
      if(hashlib.sha512(str(pw)).hexdigest() == admin[0][1]):
         with open(os.getcwd() + "/../../metadata/lastlogin.txt", "w") as last:
            last.write(username + ' ' + pw)
         root.deiconify()
         window.destroy()
      else:
         tkMessageBox.showwarning(title="Error", message="Invalid password. Please try again.")
   except:
      tkMessageBox.showwarning(title="Error", message="Authentication failed. Please try again.")

#Database Functions
#------------------------------------------------------
def add_entry(fn_entry, ln_entry, pw_entry, flag, db, db_list):
   '''
   Checks fields for entry, then makes a sql query with the user input.
   Also allows the user to interface with the database table directly.
   '''
   global mode
   #Ensure correct input
   if(flag == 0 and fn_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid first name.")
   elif(flag == 1 and fn_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid admin name.")
   elif(flag == 0 and ln_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid last name.")
   elif(flag == 0 and pw_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid username.")
   elif(flag == 1 and pw_entry.get() == ''):
      tkMessageBox.showwarning(title="Error", message="Please enter a valid password.")
   elif(' ' in str(fn_entry.get())) or (' ' in str(ln_entry.get())) or (' ' in str(pw_entry.get())):
      tkMessageBox.showwarning(title="Error", message="Spaces are not allowed in login information.")
   else:
      #Add user
      if(flag == 0):
         path = os.getcwd() + "/../../data/" + pw_entry.get() + "/"
         if(os.path.isdir(path) == False):
            tkMessageBox.showwarning(title="Error", message="Please take some pictures to associate with the new user.")
         elif(len(os.listdir(path)) < 12):
            tkMessageBox.showwarning(title="Error", message="Please take more pictures. (12 required, " + str(len(os.listdir(path))) + " current)")
         else:
            #Give text field input to the database to create a new user
            db.addUser(fn_entry.get(), ln_entry.get(), pw_entry.get())
            switch_mode(0, db_list)
      #Add admin
      elif(flag == 1):
         db.addAdmin(fn_entry.get(), hashlib.sha512(pw_entry.get()).hexdigest())
         switch_mode(1, db_list)
      fn_entry.delete(0, 'end')
      ln_entry.delete(0, 'end')
      pw_entry.delete(0, 'end')

def delete_entry(curSelection, db, db_list):
   '''
   Removes the selected table entry from the database.
   '''
   try:
      if((curSelection != ()) and (curSelection[0] != '0')):
         cur = str(db_list.get(curSelection))
         #Remove from user table
         if mode == 0:
            (fn, ln, pw) = cur.split()
            db.deleteUser(pw)
            try:
               #Clear the user's pictures
               shutil.rmtree(str(os.getcwd()) + "/../../data/"+pw+"/")
            except:
               pass
            refresh(0, db_list)
         #Remove from admin table
         if mode == 1:
            (username, pw) = cur.split()
            db.delAdmin(username)
            refresh(1, db_list)
      else:
         tkMessageBox.showwarning(title="Error", message="Please select a valid entry from the list.")
   except(IndexError):
      pass

#GUI configuration functions
#------------------------------------------------------
def configure_main_window():
   '''
   Configures the root window component.
   '''
   #Resize window and lock it to preserve component positions
   root.geometry("1150x400")
   root.resizable(width=False, height=False)
   root.configure(background="#EE8")
   root.title("In Yo Face Admin Tools")

def configure_fields():
   '''
   Configures the fields for user entry.
   '''
   #First name
   fn_label = tk.Label(master=root, text='First Name/Admin Name', background="#EE8")
   fn_label.grid(row=3, column=3)
   fn_entry = tk.Entry(master=root, width=20)
   fn_entry.grid(row=3, column=4, padx=30)

   #Last name
   ln_label = tk.Label(master=root, text='Last Name', background="#EE8")
   ln_label.grid(row=4, column=3)
   ln_entry = tk.Entry(master=root, width=20)
   ln_entry.grid(row=4, column=4, padx=30)

   #Password
   pw_label = tk.Label(master=root, text='Username/ Admin Password', background="#EE8")
   pw_label.grid(row=5, column=3)
   pw_entry = tk.Entry(master=root, width=20, show='*')
   pw_entry.grid(row=5, column=4, padx=30)

   return (fn_entry, ln_entry, pw_entry)

def configure_image_window(queue, parent):
   '''
   Configures the image window for the video feed.
   '''
   #Video feed lavel
   image_label = tk.Label(master=root)
   image_label.grid(row=3, column=0, rowspan=5,)

   root.after(0, func=lambda: update_all(image_label, queue, parent))

def configure_db_list():
   '''
   Creates a listbox to display the database's current state.
   '''
   #Scrollbar
   scrollbar = tk.Scrollbar(master=root, orient="vertical")
   scrollbar.grid(row=3, column=10, rowspan=6, sticky="N"+"S")

   #Database table
   db_list = tk.Listbox(master=root, selectmode="SINGLE", height=16,
                        width=50, yscrollcommand=scrollbar.set)
   db_list.grid(row=3, column=7, rowspan=6, columnspan=3)

   #Toggle to user table
   usermode_btn = tk.Button(master=root, text="Users", width=20, command=lambda:switch_mode(0, db_list))
   usermode_btn.grid(row=9, column=7)

   #Toggle to admin table
   adminmode_btn = tk.Button(master=root, text="Admins", width=20, command=lambda:switch_mode(1, db_list))
   adminmode_btn.grid(row=9, column=8)

   #Attach scrollbar and initialize to user table
   scrollbar.config(command=db_list.yview)
   refresh(0, db_list)
   return db_list

def configure_buttons(fn_entry, ln_entry, pw_entry, db, queue, child, db_list):
   '''
   Configures the buttons that allow user interactivity.
   '''
   #Add user
   adduser_btn = tk.Button(master=root, command=lambda:add_entry(fn_entry, ln_entry, pw_entry, 0, db, db_list), background="Green", width=15, text="Add User")
   adduser_btn.grid(row=6, column=3)

   #Add admin
   addadmin_btn = tk.Button(master=root, command=lambda:add_entry(fn_entry, ln_entry, pw_entry, 1, db, db_list), background="#44DDDD", width=15, text="Add Admin")
   addadmin_btn.grid(row=7, column=3)

   #Delete selection
   delete_btn = tk.Button(master=root, command=lambda:delete_entry(db_list.curselection(), db, db_list), background="Orange", width=15, text="Delete Selection")
   delete_btn.grid(row=6, column=4)

   #Quit
   quit_btn = tk.Button(master=root, command=lambda:quit(root, p, db), background="#EE5555", width=15, text="Quit")
   quit_btn.grid(row=7, column=4)

   #Take a picture
   capture_btn = tk.Button(master=root, command=lambda:child.send(True), background="#7777FF", text="Take a picture!")
   capture_btn.grid(row=9, column=0)

#Misc Functions
#------------------------------------------------------
def read_fields():
   '''
   Reads the text fields on the GUI and returns them as a single tuple.
   '''
   return (fn_entry.get(), ln_entry.get(), pw_entry.get())

def clean_data(db):
   '''
   Deletes all the partially full image folders or ones
   that are no longer in the database.
   '''
   #Get rid of extraneous folders in the current directory
   for entry in os.listdir(os.getcwd()):
      if(os.path.isdir(entry)):
         shutil.rmtree((os.getcwd()) + str(entry))

   data_path = os.getcwd() + "/../../data/"
   for entry in os.listdir(data_path):
      #Get rid of folders with less that 12 pictures
      if(os.path.isdir(str(data_path) + str(entry))):
         if(len(os.listdir(str(data_path) + str(entry))) < 12):
            shutil.rmtree(str(data_path) + str(entry))
      #Get rid of all non-directory entries in the data folder
      else:
         os.remove(str(data_path) + str(entry))

      #Get rid of all users the database can't find
      if(db.getUser(entry) == ()):
         shutil.rmtree(str(data_path) + str(entry))

def switch_mode(flag, db_list):
   '''
   Toggles between editing the user and admin table.
   '''
   global mode
   #User mode
   if flag == 0:
      mode = 0
   #Admin mode
   if flag == 1:
      mode = 1
   refresh(mode, db_list)

def refresh(mode, db_list):
   '''
   Updates the listbox to stay current with the database.
   '''
   #Refresh user table
   if mode == 0:
      user_list = db.getUsers()
      db_list.delete(0, db_list.size())
      db_list.insert(0, "USERS - FIRSTNAME    LASTNAME    USERNAME")
      try:
         for (fn, ln, user) in user_list:
            db_list.insert(db_list.size(), fn + " " + ln + " " + user)
      except(TypeError):
         pass
   #Refresh admin table
   if mode == 1:
      admin_list = db.getAdmins()
      db_list.delete(0, db_list.size())
      db_list.insert(0, "ADMINS - USERNAME    PASSWORD")
      try:
         for (username, pw) in admin_list:
            db_list.insert(db_list.size(), username + " " + pw)
      except(TypeError):
         pass

def quit(root, process, db):
   '''
   Kills the GUI and the related video feed process.
   '''
   try:
      #Get rid of useless folders
      clean_data(db)
   except:
      pass
   #Make a new learner
   learnerGenerator.createLearner()
   #Push new learner to the FTP server
   ftp = FTPLearner.FTPLearner()
   ftp.pushLearner()
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
   db = server.Server()
   db.connect()
   db_list = configure_db_list()
   configure_buttons(fn_entry, ln_entry, pw_entry, db, queue, child, db_list)
   
   p.start()
   root.withdraw()
   auth_admin(root, p, db)
   root.protocol('WM_DELETE_WINDOW', lambda:quit(root, p, db))
   root.mainloop()
