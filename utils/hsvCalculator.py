
import cvzone
from cvzone.ColorModule import ColorFinder
import cv2
import numpy as np

 
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
 
success, img = cap.read()
h, w, _ = img.shape
print(h, w, _)
myColorFinder = ColorFinder(True)
# hsvVals ={'hmin': 11, 'smin': 79, 'vmin': 63, 'hmax': 51, 'smax': 213, 'vmax': 223}
# hsvVals ={'hmin': 17, 'smin': 28, 'vmin': 186, 'hmax': 47, 'smax': 112, 'vmax': 255}
# hsvVals={'hmin': 8, 'smin': 88, 'vmin': 51, 'hmax': 25, 'smax': 255, 'vmax': 255}
hsvVals={'hmin': 11, 'smin': 82, 'vmin': 75, 'hmax': 42, 'smax': 205, 'vmax': 192}
img=cv2.imread("images/ball_yellow.jpg")
pers_values=np.load('./pers_values.npy')
while True:
    success, img = cap.read()
    # pts1 = np.float32([[132, 155], [875, 159],	[29, 610], [921, 604]])
    pts1 = np.float32(pers_values)
    pts2 = np.float32([[0, 0], [1280, 0],[0, 720], [1280, 720]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img = cv2.warpPerspective(img, matrix, (1280, 720))
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask)

 
    imgStack = cvzone.stackImages([img, imgColor], 2, 0.5)
    cv2.imshow("Image", imgStack)

    cv2.waitKey(1)