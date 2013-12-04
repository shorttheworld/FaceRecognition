#Server Connections for Database

import MySQLdb as SQL


class Server: 
		
	def connect(self):
                try:
                      last = open("../../metadata/dbconfig.txt", "r")
                      last_str = last.read().split()
                except:
                      last_str = ''

                if(last_str == ''):
                      user = 'root'
                      passwd = ''
                      host = 'localhost'
                elif(len(last_str) == 2):
                      user = last_str[0]
                      passwd = ''
                      host = last_str[1]
                elif(len(last_str) == 3):
                      user = last_str[0]
                      passwd = last_str[1]
                      host = last_str[2]
                
		self.db=SQL.connect(host=host, user=user,passwd=passwd,db='inyoface', port=3306)
		self.cursor=self.db.cursor()
		
	def addUser(self, fn, ln, username, active=1):
		sql="INSERT INTO user (FIRST_NAME, LAST_NAME, USERNAME, ACTIVE) VALUES (%s,%s, %s, %s)"
		self.cursor.execute(sql, (fn,ln,username,active))
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

        def getMapping(self):
		sql="SELECT user_index,username FROM user"
		self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.fetchall()
		
	def getUsers(self):
		sql="SELECT first_name,last_name,username FROM user"
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
                sql="SELECT * FROM admin WHERE USERNAME='"+user+"'"
                self.cursor.execute(sql)
                self.db.commit()
                return self.cursor.fetchall()
