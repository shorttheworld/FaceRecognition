#!/usr/bin/python

import numpy as np
from multiprocessing import Process, Queue
from Queue import Empty
import cv2
from PIL import Image, ImageTk
import time
import Tkinter as tk

#tkinter GUI functions----------------------------------------------------------
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

#multiprocessing image processing functions-------------------------------------
def image_capture(queue):
   vidFile = cv2.VideoCapture(0)

   while True:
      try:
         flag, frame = vidFile.read() # what does flag mean?
         if flag==0:
            break
         queue.put(frame) 	# why is this loading frames onto the queue? because the thread might not
         					# be able to display frames quickly enough?
         cv2.waitKey(20)
      except:
         continue

def enter_text(entry):
	pin = entry.get()
	print pin

if __name__ == '__main__':
   root = tk.Tk()

   image_label = tk.Label(master=root)# label for the video frame
   image_label.pack()

   #start image capture process
   queue = Queue()
   p = Process(target=image_capture, args=(queue,)) # why is queue passed in as a parameter like this?
   p.start()
   
   quit_button = tk.Button(master=root, text='Quit', command=lambda: quit(root,p)) # what is lambda?
   quit_button.pack()

   entry = tk.Entry(master=root, show='*')
   entry.pack()

   enter_button = tk.Button(master=root, text='Enter', command=lambda: enter_text(entry))
   enter_button.pack()
   
   # setup the update callback
   root.after(0, func=lambda: update_all(root, image_label, queue)) # what is "after"?
   root.mainloop()