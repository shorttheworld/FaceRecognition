import cv2

def goodOrBad(img,cascade):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False
    else:
        box(rects, img)
        return True

def box(rects, img):
    
    crop_img = img[(rects[0][1]-10):(rects[0][1] + 214), (rects[0][0]+10):(rects[0][0]+194)]
    newX, newY = crop_img.shape[1]/2, crop_img.shape[0]/2
    crop_img = cv2.resize(crop_img,(newX,newY))
    cv2.imwrite('grayscale.jpg', crop_img)