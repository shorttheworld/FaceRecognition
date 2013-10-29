#Defines a class for interacting with the DB for In Yo Face's project

import MySQLdb
import Tkinter as tk
import tkFileDialog

def connect():
	try:
		return MySQLdb.connect(host='localhost', user='root', passwd='', db='inyoface', port=3306)
	except:
		print("DB connection failed")

class DB:
	
	def __init__(self):
		self.db=connect()
		if self.db==None:
			exit()
		self.cursor=self.db.cursor()
		#self.setupDB()
		#self.addUser()
		#self.addAdmin()
		self.uploadLearner()
		
	def addUser(self):
		first=raw_input("First name: ")
		last=raw_input("Last name: ")
		self.username=raw_input("Username: ")
		path=raw_input("Img_Path: ")
		sql="INSERT INTO user (FIRST_NAME, LAST_NAME, USERNAME, IMG_PATH) VALUES (%s,%s, %s, %s)"
		self.cursor.execute(sql, (first,last,self.username,path))
		self.db.commit()
		
	def addAdmin(self):
		self.addUser()
		pass_hash=raw_input("Password: ")
		sql="INSERT INTO admin (USERNAME, PASS_HASH) VALUES (%s,%s)"
		self.cursor.execute(sql, (self.username,pass_hash))
		self.db.commit()
		
		#Working on this now. -Solace
	def uploadLearner(self):
		rootWin=tk.Tk()
		file=tkFileDialog.askopenfile('r')
		sql="INSERT INTO learner (LEARNER) VALUES (%s)"
		file=file.read()
		print(len(file))
		self.cursor.execute(sql, (file))
		self.db.commit()
	
	"""	
	def setupDB(self):
		sql=read(open('inyoface.sql'))
		self.cursor.execute(sql)
		print('Done')
	"""
db=DB()