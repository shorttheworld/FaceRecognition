import os
from cv2 import *


class Controller():

    def __init__(self):
        #self.__det = FaceDetector()
        #self.__rec = FaceRecognizer()
        self.d = {}
        self.d[9001] = "Chris"
        self.validatePin(9001)
        self.addPics()
        self.curPic = None
        self.result = None

    def receivePic(self, pic):
        self.curPic = pic

    def validatePin(self, pin):
        for key in self.d.keys():
            if key == pin:
                return True

        return False
        

    def __validateFace(self):
        '''
        self.result = self.__det.detectFace(curPic)

        if result.noResult():
            

        else if result.noFace():
            

        else if result.match():
            

        else if result.noMatch():
            

        else if result.multFaces():

        
        '''
        return false

    def __recognizeFace(self):
        '''
        
        
        
        '''
        return false
    
#adds idNum and pictureLits to dictionary
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
