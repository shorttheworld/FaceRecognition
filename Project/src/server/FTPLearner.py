#FTPLearner.py

from ftplib import FTP

"""
Pushes learner to FTP server to pulling to clients
"""

class FTPLearner:
	
	def __init__(self):
		ftplogin=open('../../metadata/ftplogin.txt', 'r')
		self.username, self.password, self.host=ftplogin.read().split()
		ftplogin.close()
		
	def pushLearner(self):
		learner=open('../../metadata/learner.xml','r')
		self.connect()
		self.ftp.storbinary('STOR learner.xml',learner)
		self.ftp.quit()
		learner.close()
		
	def connect(self):
		self.ftp=FTP(self.host, self.username, self.password)
		