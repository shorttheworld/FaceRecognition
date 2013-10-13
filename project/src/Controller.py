import os
from cv2 import *


class Controller():

    def __init__(self):
        #self.__det = FaceDetector()
        #self.__rec = FaceRecognizer()
        self.d = {}
        #self.d[9001] = "Chris"
        #self.validatePin(9001)
        self.addPics()
        self.curPic = None
        self.result = None
        self.pin = None

    def receivePic(self, pic, pin):
        self.curPic = pic
        self.pin = pin
        if self.validatePin(self.pin) == False:
            print("The desired pin was not found in the database. Please try again.")
            return false
        
        self.result = self.validateFace()
        '''
        if temp.noResult():
            print("Error: Result not valid. Please take another picture.")
            return false
            
        elif temp.noFace():
            print("No face was detected. Please reposition yourself in front of the camera")
            return false

        elif temp.noMatch():
            print("No valid faces detected.")
            return false

        elif temp.multFaces():
            print("Multiple faces detected. Please take a new picture.")
            return false

        elif temp.match():
            print("Valid face detected. Checking credentials.")
                matchResult = self.recognizeFace()
                if matchResult.personID() == None:
                print("No facial matches were found. Please try again.")
                return false

                elif matchResult.personID() != self.pin:
                print("Facial match failed. Please try again.")
                return false

                elif matchResult.personID() == self.pin:
                print("Match found. Welcome!")
                return true
        '''
        return false

    def validatePin(self, pin):
        for key in self.d.keys():
            if key == pin:
                return True

        return False
        

    def __validateFace(self):
        #return self.__det.detectFace(curPic)
        return false

    def __recognizeFace(self):
        #return self.__rec.recognizeImage(self.result)
        return false
    
    #adds idNum and pictureList to dictionary
    def addPics(self):
        path = os.getcwd()
        path = path.strip("\Project")
        path = path + "\sample_faces"
       
        idNum = 100
        for folder in os.listdir(path):
            temp = path
            temp = temp + "\\" + folder + "\small"
            fileList = os.listdir(temp)
            picList = []
            
            
            for f in fileList:
                picList.append(imread(temp + "\\" + f))
            (self.d)[idNum] = picList
            
            idNum = idNum + 1


        
        #here is how to show a picture
        #namedWindow("window", CV_WINDOW_AUTOSIZE)
        #imshow("window", pic)
        #waitKey(10)
