#Server Connections for Database

import MySQLdb as SQL


class Server: 
	""""
	Server class for handling connections to and from database
	"""
	def connect(self):
		""""
		Connect to the database using the file credentials stored in dbconfig.txt
		"""
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
		"""
		Add a user
		"""
		sql="INSERT INTO user (FIRST_NAME, LAST_NAME, USERNAME, ACTIVE) VALUES (%s,%s, %s, %s)"
		self.cursor.execute(sql, (fn,ln,username,active))
		self.db.commit()
		
	def deleteUser(self, username):
		"""
		Delete a user
		"""
		sql="DELETE FROM user WHERE USERNAME='"+username+"'"
		self.cursor.execute(sql)
		self.db.commit()
	
	def addAdmin(self,user, passwd):
		"""
		Add an admin
		"""
		sql="INSERT INTO admin (USERNAME, PASSWORD) VALUES (%s, %s)"
		self.cursor.execute(sql, (user, passwd))
		self.db.commit()
		
	def delAdmin(self, user):
		"""
		Delete an admin
		"""
		sql="DELETE FROM admin WHERE USERNAME='"+user+"'"
		self.cursor.execute(sql)
		self.db.commit()

        def getMapping(self):
                """
                Get a mapping for the users to the file system
                """
                sql="SELECT user_index,username FROM user"
                self.cursor.execute(sql)
                self.db.commit()
                return self.cursor.fetchall()
		
	def getUsers(self):
		"""
		Get all the users
		"""
		sql="SELECT first_name,last_name,username FROM user"
		self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.fetchall()
	def getUser(self, user):
		"""
		Get a specific User
		"""
                sql="SELECT * FROM user WHERE USERNAME='"+user+"'"
                self.cursor.execute(sql)
                self.db.commit()
                return self.cursor.fetchall()
        def getUserInfo(self, username):
                sql="SELECT first_name, last_name FROM user WHERE username=%s"
                self.cursor.execute(sql, (username))
                self.db.commit()
                result = self.cursor.fetchall()[0]
                return result[0] + " " + result[1]

        def getUserActive(self, username):
                """
                Get a specific User
                """
                sql="SELECT active FROM user WHERE username=%s"
                self.cursor.execute(sql, (username))
                self.db.commit()
                active = 0
                try:
                        active = self.cursor.fetchall()[0][0]
                except:
                        pass
                return (active == 1) 
		
	def getAdmins(self):
		"""
		Get all the Admins
		"""
		sql="SELECT * FROM admin"
		self.cursor.execute(sql)
		self.db.commit()
		return self.cursor.fetchall()

	def getAdmin(self, user):
		"""
		Get a specific admin
		"""
                sql="SELECT * FROM admin WHERE USERNAME='"+user+"'"
                self.cursor.execute(sql)
                self.db.commit()
                return self.cursor.fetchall()
