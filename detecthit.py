import cv2
import numpy as np
from balloonhit import *


def detectHit(img,bbox):
    imgBalloonList=splitBalloons(img,bbox)
    showballoons(imgBalloonList)
    return img

def splitBalloons(img,bbox):
    imgBalloonList=[]
    for b in bbox:
        x1,y1,x2,y2=b[0],b[1],b[0]+b[2],b[1]+b[3]
        imgBalloonList.append(img[y1[0]:y2[0], x1[0]:x2[0]])
    return imgBalloonList

def showballoons(imgBalloonList):
    for x, im in enumerate(imgBalloonList):
        cv2.imshow(str(x),im)
