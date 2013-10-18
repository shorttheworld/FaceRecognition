#!/usr/bin/python

import MySQLdb

def setup_db():
	db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="FacialRecognition") 
	global cur
	cur = db.cursor() 

def get_name(pin):
	cmd = "SELECT first_name, last_name FROM person WHERE pin=" + str(pin)
	cur.execute(cmd)
	person = cur.fetchone()

	print person[0] + " " + person[1]

if __name__ == '__main__':
	setup_db()
	get_name(12345);
	#curr.execute("INSERT INTO person (pin, first_name, last_name, admin) VALUES (69696, 'Ryan', 'Hollis', true);")