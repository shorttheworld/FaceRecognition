import cv2

def goodOrBad(img,cascade, num):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False
    else:
        box(rects, img, num)
        return True

def box(rects, img, num):
    
    crop_img = img[(rects[0][1]-20):(rects[0][1] + 204), (rects[0][0]-5):(rects[0][0]+179)]
    if len(crop_img) == 224 and len(crop_img[0]) == 184:
        newX, newY = crop_img.shape[1]/2, crop_img.shape[0]/2
        crop_img = cv2.resize(crop_img,(newX,newY))
        cv2.imwrite("victim/"+str(num)+".jpg" , crop_img)