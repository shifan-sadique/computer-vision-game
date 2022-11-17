
import cvzone
from cvzone.ColorModule import ColorFinder
import cv2

 
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
 
success, img = cap.read()
h, w, _ = img.shape
print(h, w, _)
myColorFinder = ColorFinder(True)
hsvVals ={'hmin': 11, 'smin': 79, 'vmin': 63, 'hmax': 51, 'smax': 213, 'vmax': 223}
img=cv2.imread("images/ball_yellow.jpg")
while True:
    success, img = cap.read()
 
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask)

 
    imgStack = cvzone.stackImages([img, imgColor], 2, 0.5)
    cv2.imshow("Image", imgStack)

    cv2.waitKey(1)