#Server Connections for Database and FTP

import MySQLdb as SQL
from ftplib import FTP_TLS as FTP



class Server:
	def __init__(self, host, user, passwd):
		self.db=SQL.connect(host=host, user=user,passwd=passwd,db='inyoface', port=3306)
		self.cursor=self.db.cursor()
		
		self.ftp=FTP(host,user,passwd)
		self.ftp.prot_p()
		
	def addUser(self, fn, ln, pw, piclist):
		sql="INSERT INTO user (FIRST_NAME, LAST_NAME, PASSWORD) VALUES (%s,%s, %s)"
		self.cursor.execute(sql, (fn,ln,pw,path))
		self.db.commit()
		
		self.ftpConnect()
		self.ftp.cwd("./data/") #switch to data folder
		self.ftp.mkdir(pw) #create a folder for the user
		ftp.cwd(pw)
		for pic in piclist:
			self.ftp.storbinary("STOR "+pic.name, pic)
	
	def deleteUser(self, pw):
		sql="DELETE FROM user WHERE PASSWORD='"+pw+"'"
		self.cursor.execute(sql)
		self.db.commit()
		
		self.ftpConnect()
		ftp.cwd("./data/")
		self.ftp.rmd(pw)
	
	def sendLearner(self, learner):
		self.ftp_Connect()
		ftp.cwd("./metadata/")
		self.ftp.storbinary("STOR "+lerner.name,learner)
		
	def addAdmin(self,user, passwd):
		sql="INSERT INTO admin (USERNAME, PASSWORD) VALUES (%s, %s)"
		self.cursor.execute(sql, (user, passwd))
		self.db.commit()
		
	def delAdmin(self, user):
		sql="DELETE FROM admin WHERE USERNAME='"+user"'"
		self.cursor.execute(sql)
		self.db.commit()
		
	def ftpConnect(self):
		self.ftp.login(self.host, self.user, self.passwd) #Resestablish the ftp connection if necessary
		self.ftp.prot_p() #Secure the connection		
		
		
		
		
		