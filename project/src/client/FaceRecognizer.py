#!/usr/bin/python
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

    def __init__(self):
        self.imageTable = {}
        self.learnerList = None
        self.retVal = None
        self.learner = cv2.createEigenFaceRecognizer(40,35000.0)
        if(os.path.isfile("../metadata/learner.xml")):
                self.learner.load("../metadata/learner.xml")
                if(os.path.isfile('../metadata/map.p')):
                    self.imageTable = pickle.load(open('../metadata/map.p','rb'))
                self.retVal = self.testLearner(self.learner)
        else:
                self.train('../data')
        #print self.learner.getDouble("threshold")
        #self.learner.set("threshold",2500.0)

    def extractData(self,path,learner = None):
        X = []
        Y = []
        c = 0


        for subdirs in os.listdir(path):
            curdir = os.listdir(os.path.join(path,subdirs))
            curpath = os.path.join(path,subdirs)
            #if subdirs != 'hannah':
            for image in os.listdir(curpath):
                imagePath = os.path.join(curpath,image)
                print imagePath
                im = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
                X.append(np.asarray(im,dtype=np.uint8))
                Y.append(c)
            self.imageTable[c] = subdirs
            c = c + 1

            print subdirs
        pickle.dump(self.imageTable,open("../metadata/map.p","wb"))
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
        learner.save("../metadata/learner.xml")
        self.testLearner(learner)

        
    def testLearner(self,learner):
        peopleList = []
        confList = []

        recognizedPeople={}
            
        for image in os.listdir("victim/"):
                imgPath = os.path.join("victim/", image)
                testImage = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
                [lab, conf] = learner.predict(np.asarray(testImage))
                peopleList.append(self.imageTable.get(lab))
                confList.append(conf)
        for i in range(0, len(peopleList)):
                if(confList[i] < 3500):
                    if peopleList[i] in recognizedPeople:
                        recognizedPeople[peopleList[i]] = recognizedPeople[peopleList[i]] + 1
                    else:
                        recognizedPeople[peopleList[i]] = 1

        result = ""
        if (0 < len(recognizedPeople)):
            result = max(recognizedPeople, key=recognizedPeople.get)

        return result

    def result(self):
        return self.retVal

c = FaceRecognizer()
print c.result()
