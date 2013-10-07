import os
import sys
import cv2
import numpy as np
import pickle

class FaceRecognizer:
	# This class will be responsible for testing the learner
	# on the image given. There will be multiple learners
	# depending on the 'pin' the appropriate learner
	# will be queried.

    def extractData(self,path,learner = None):
        X = []
        Y = []
        c = 0


        for subdirs in os.listdir(path):
            curdir = os.listdir(os.path.join(path,subdirs))
            curpath = os.path.join(path,subdirs)
            for imageFolder in curdir:
                if imageFolder == 'small':
                    imagePath = os.path.join(curpath,imageFolder)
                    for image in os.listdir(imagePath):
                        img = os.path.join(imagePath,image)
                        im = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
                        X.append(np.asarray(im,dtype=np.uint8))
                        Y.append(c)
            self.imageTable[c] = subdirs
            c = c + 1

            print subdirs

        return [X,Y]                



    #This method will train the learner on the images given
    # by path. The additional parameter learner can train
    # a certain instance of the learner on the images
    def train(self,pathToImages, learnerID = None):
        learner = self.learner
        if (learnerID is not None):
            learner = self.learnerList[learnerID]
        else:
            learner = self.learner

        [X,Y] = self.extractData(pathToImages)
        y = np.asarray(Y,dtype=np.int32)
        print type(X)
        print len(X)
        learner.train(np.asarray(X),np.asarray(y))
        testImage  = cv2.imread('../12.pgm', cv2.IMREAD_GRAYSCALE)
        [lab,conf] = learner.predict(np.asarray(testImage))
        print "Found ", self.imageTable.get(lab)
        print "Confidence " , conf



    def __init__(self):
		self.imageTable = {}
		self.learnerList = None
		self.learner = cv2.createEigenFaceRecognizer()
		if(os.path.isfile('map.p')):
			self.imageTable = pickle.load(open('map.p','rb'))


c = FaceRecognizer()
c.train('/home/akbar/Desktop/FaceRecognition/FaceRecognition/Data/1')

	
