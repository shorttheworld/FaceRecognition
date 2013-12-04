#FTPLearner.py

from ftplib import FTP
import tkMessageBox

"""
Pushes learner to FTP server to pulling to clients
"""

class FTPLearner:
	
	def __init__(self):
                try:
                        ftplogin=open('../../metadata/ftplogin.txt', 'r')
                except Exception:
                        tkMessageBox.showwarning(title="Error", message="An error " +
                        "occurred while trying to recover login data.")
		self.username, self.password, self.host=ftplogin.read().split()
		ftplogin.close()
		
	def pushLearner(self):
                try:
                        learner=open('../../metadata/learner.xml','r')
                except Exception:
                        tkMessageBox.showwarning(title="Error", message="An error " +
                        "occurred while trying to update the learner")
		self.connect()
		self.ftp.storbinary('STOR learner.xml',learner)
		self.ftp.quit()
		learner.close()
		
	def connect(self):
                try:
        		self.ftp=FTP(self.host, self.username, self.password)
        	except Exception:
                        tkMessageBox.showwarning(title="Error", message="An error " +
                        "occurred while trying to connect to the FTP server")
		
