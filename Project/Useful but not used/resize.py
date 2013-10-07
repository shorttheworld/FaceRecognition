import cv2
filename = "lena.jpg"
oriimage = cv2.imread(filename)
newx,newy = oriimage.shape[1]/2,oriimage.shape[0]/2 #new size (w,h)
newimage = cv2.resize(oriimage,(newx,newy))
cv2.imshow("original image",oriimage)
cv2.imshow("resize image",newimage)
cv2.waitKey(0)