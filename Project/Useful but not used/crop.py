import cv2
img = cv2.imread("lena.jpg")
crop_img = img[40:400, 100:430]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)