#This script will go into the database and pull all users out
# once it has done this it will use the 'data' folder and create
# a learner and use the auto increment values in the user table
# as a way to map foldernames to their indices.

####NOTICE#####

# The assumption here is that all the entries in the 'user' table in the database
# have their matching folders in the data directory. If this condition is not met
# the behavior of this program is undefined

####NOTICE#####
import os,sys,cv2,numpy as np
import server

#This method is responsible for creating the learner
# deafault path is set to '../../data/'
def createLearner(path = "../../data/"):
	db = server.Server()
	db.connect()
	tup = db.getMapping()
	# Reverse the mapping so we can map folder names to their index value
	mapping = dict(map(reversed,tup))
	[X,Y] = extractData(path,mapping)
	y = np.asarray(Y,dtype=np.int32)
	learner = cv2.createEigenFaceRecognizer(40,35000.0)
	learner.train(np.asarray(X),np.asarray(y))
	learner.save("../../metadata/learner.xml")

#This method is responsible for extracting images from the
# data folder and then creating in a format which
# the learner can train on
def extractData(path,map):
	X = []
	Y = []
	c = 0
	for subdirs in os.listdir(path):
		curdir = os.listdir(os.path.join(path,subdirs))
		curpath = os.path.join(path,subdirs)
		for image in os.listdir(curpath):
			imagePath = os.path.join(curpath,image)
			im = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
			X.append(np.asarray(im,dtype=np.uint8))
			Y.append(int(map.get(subdirs)))
	return [X,Y] 
	
#Uncomment the line below if you want this script to run from terminal	
createLearner()
