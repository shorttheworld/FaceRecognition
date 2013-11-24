#Server Connections for Database and FTP

import MySQLdb as SQL
from ftplib import FTP



class Server:
	def __init__(self, host, user, passwd, ftpuser, ftppw):
                self.host=host
                self.ftpuser=ftpuser
                self.ftppw=ftppw
                
		self.db=SQL.connect(host=host, user=user,passwd=passwd,db='inyoface', port=3306)
		self.cursor=self.db.cursor()
		self.ftp=None
		self.ftp=self.ftpConnect()
		#self.ftp.prot_p()
		
	def addUser(self, fn, ln, username):
		sql="INSERT INTO user (FIRST_NAME, LAST_NAME, USERNAME) VALUES (%s,%s, %s)"
		self.cursor.execute(sql, (fn,ln,username))
		self.db.commit()
	
	def deleteUser(self, username):
		sql="DELETE FROM user WHERE USERNAME='"+username+"'"
		self.cursor.execute(sql)
		self.db.commit()

		'''
		self.ftpConnect()
		ftp.cwd("./data/")
		self.ftp.rmd(pw)
		'''
	
	def sendLearner(self, learner):
		self.ftp_Connect()
		ftp.cwd("./metadata/")
		self.ftp.storbinary("STOR "+learner.name,learner)
		
	def addAdmin(self,user, passwd):
		sql="INSERT INTO admin (USERNAME, PASSWORD) VALUES (%s, %s)"
		self.cursor.execute(sql, (user, passwd))
		self.db.commit()
		
	def delAdmin(self, user):
		sql="DELETE FROM admin WHERE USERNAME='"+user+"'"
		self.cursor.execute(sql)
		self.db.commit()
		
	def getUsers(self):
		sql="SELECT * FROM user"
		self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.fetchall()
		
	def getAdmins(self):
		sql="SELECT * FROM admin"
		self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.fetchall()
		
	def ftpConnect(self):
                if self.ftp==None: #Create FTP object if none exists
                        return FTP(self.host, self.ftpuser, self.ftppw)
		self.ftp.login(self.host, self.ftpuser, self.ftppw) #Resestablish the ftp connection if necessary
		
