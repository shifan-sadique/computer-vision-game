
import cvzone
from cvzone.ColorModule import ColorFinder
import cv2

 
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
 
success, img = cap.read()
h, w, _ = img.shape
print(h, w, _)
myColorFinder = ColorFinder(False)
hsvVals ={'hmin': 148, 'smin': 104, 'vmin': 1, 'hmax': 163, 'smax': 231, 'vmax': 217}

while True:
    success, img = cap.read()
    # img = image
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask)
    # print(contours)
    if contours:
        data = contours[0]['center'][0], \
               h - contours[0]['center'][1], \
               int(contours[0]['area'])
        # print(contours[0]['center'])
        # break
        
 
    # imgStack = cvzone.stackImages([img, imgColor], 2, 0.5)
    # cv2.imshow("Image", imgStack)
    imgContour = cv2.resize(imgContour, (0, 0), None, 0.5, 0.5)
    cv2.imshow("ImageContour", imgContour)
    cv2.waitKey(1)