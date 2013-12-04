#Update Learner

from ftplib import FTP

class LearnerUpdater:
	def __init__(self):
		self.buff=[]
		ftplogin=open('../../metadata/ftplogin.txt', 'r')
		self.username, self.password, self.host=ftplogin.read().split()
		ftplogin.close()
		
	def getLearner(self, host):
		self.connect()
		self.ftp.retrbinary('RETR learner.xml', self.buffer)
		file=open("../../metadata/learner.xml","a")
		for item in self.buff:
			file.write(str(item))
		file.close()
		self.ftp.quit()
		
	def buffer(self, data):
		self.buff.append(data)
		
	def connect(self):
		self.ftp=FTP(self.host, self.username, self.password)