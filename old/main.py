import cv2
from detecthit import *
import cv2
img=cv2.imread("raw.png")
imgBalloon,bbox=findballoons(img)
img=detectHit(img,bbox)
cv2.imshow("imageshow",img)
cv2.waitKey(0)
