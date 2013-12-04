#!/usr/bin/python
import os
import sys
import cv2
import numpy as np
import server

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
        db = server.Server()
        db.connect()
        tup = db.getMapping()
        self.imageTable = dict(tup)
        if(os.path.isfile("../../metadata/learner.xml")):
                self.learner.load("../../metadata/learner.xml")
                self.retVal = self.testLearner(self.learner)
        else:
			print "Learner not found, please make sure learner.xml is in the appropriate file"

        
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


