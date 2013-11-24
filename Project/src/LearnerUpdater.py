#Update Learner

import ftplib

class LearnerUpdater:
	def __init__(self):
		self.buff=[]
		
	def getLearner(self, host):
		ftp=ftplib.FTP(host, 'client', 'InYoFace')
		ftp.retrbinary('RETR learner.xml', self.buffer)
		file=open("../metadata/learner.xml","w")
		print(self.buff)
		for item in self.buff:
			file.write(str(item))
		file.close()
		ftp.quit()
		
	def buffer(self, data):
		self.buff.append(data)