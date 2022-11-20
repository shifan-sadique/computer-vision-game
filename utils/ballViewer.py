
import cvzone
from cvzone.ColorModule import ColorFinder
import cv2

 
cap = cv2.VideoCapture(3)
cap.set(3, 1280)
cap.set(4, 720)
 
success, img = cap.read()
h, w, _ = img.shape
print(h, w, _)
myColorFinder = ColorFinder(False)
# hsvVals ={'hmin': 148, 'smin': 104, 'vmin': 1, 'hmax': 163, 'smax': 231, 'vmax': 217}
# hsvVals ={'hmin': 8, 'smin': 88, 'vmin': 51, 'hmax': 25, 'smax': 255, 'vmax': 255}
# hsvVals={'hmin': 11, 'smin': 82, 'vmin': 75, 'hmax': 42, 'smax': 205, 'vmax': 192}
hsvVals={'hmin': 21, 'smin': 33, 'vmin': 33, 'hmax': 29, 'smax': 255, 'vmax': 200} #night class

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