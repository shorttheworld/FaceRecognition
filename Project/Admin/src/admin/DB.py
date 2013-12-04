#Defines a class for interacting with the DB for In Yo Face's project

import MySQLdb
import Tkinter as tk
import tkFileDialog

def connect():
        #Check OS here
        
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
		#self.uploadLearner()
		
	def addUser(self, fn, ln, pw):
		path="/data/" + pw
		sql="INSERT INTO user (FIRST_NAME, LAST_NAME, PASSWORD, IMG_PATH) VALUES (%s,%s, %s, %s)"
		self.cursor.execute(sql, (fn,ln,pw,path))
		self.db.commit()
		
	def addAdmin(self, fn, pw):
		#self.addUser()
		pass_hash=raw_input("Password: ")
		sql="INSERT INTO admin (USERNAME, PASS_HASH) VALUES (%s,%s)"
		self.cursor.execute(sql, (self.username,pass_hash))
		self.db.commit()
		
		#Working on this now. -Solace


        def deleteUser(self, pw):
                sql="DELETE FROM user WHERE PASSWORD='" + pw +"'"
                self.cursor.execute(sql)
                self.db.commit()

        def deleteAdmin(self, username, pw):
                #Delete an admin based off username or password(whichever you think is necessary)
                pass
        
	def uploadLearner(self):
		rootWin=tk.Tk()
		file=tkFileDialog.askopenfile('r')
		sql="INSERT INTO learner (LEARNER) VALUES (%s)"
		file=file.read()
		print(len(file))
		self.cursor.execute(sql, (file))
		self.db.commit()

	def get_users(self):
                #Return a list of users as a list of (First name, Last name, password) tuples
                pass

        def get_admins(self):
                #Return a list of admins as a list of (Username, password) tuples
                pass
	"""	
	def setupDB(self):
		sql=read(open('inyoface.sql'))
		self.cursor.execute(sql)
		print('Done')
	"""
