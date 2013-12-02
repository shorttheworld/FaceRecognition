#Server Connections for Database

import MySQLdb as SQL


class Server: 
		
	def connect(self, host, user, passwd):
		self.db=SQL.connect(host=host, user=user,passwd=passwd,db='inyoface', port=3306)
		self.cursor=self.db.cursor()
		
	def addUser(self, fn, ln, username):
		sql="INSERT INTO user (FIRST_NAME, LAST_NAME, USERNAME) VALUES (%s,%s, %s)"
		self.cursor.execute(sql, (fn,ln,username))
		self.db.commit()
		
	def deleteUser(self, username):
		sql="DELETE FROM user WHERE USERNAME='"+username+"'"
		self.cursor.execute(sql)
		self.db.commit()
	
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

	def getUser(self, user):
                sql="SELECT * FROM user WHERE USERNAME='"+user+"'"
                self.cursor.execute(sql)
                self.db.commit()
                return self.cursor.fetchall()
		
	def getAdmins(self):
		sql="SELECT * FROM admin"
		self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.fetchall()

	def getAdmin(self, user):
                sql="SELECT PASS_HASH FROM admin WHERE USERNAME='"+user+"'"
                self.cursor.execute(sql)
                self.db.commit()
                return self.cursor.fetchall()
