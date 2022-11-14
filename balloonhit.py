import numpy
import cv2
import pygame
import numpy as np

def detectscreen():
    img=cv2.imread("ball2.png")
    scale_percent = 60# percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

# resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    findballoons(resized)

def findballoons(img):
    preProcess(img)
    return img,img

def findcontours(img):
    h,w= img.shape
    imgContours=np.zeros((w,h),np.uint8)
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContours,contours,-1,(255,0,255),2)
    try: hierarchy = hierarchy[0]
    except: hierarchy = []

    # computes the bounding box for the contour, and draws it on the frame,
    for contour, hier in zip(contours, hierarchy):
        (x,y,w,h) = cv2.boundingRect(contour)
        if w > 80 and h > 80:
            cv2.rectangle(imgContours, (x,y), (x+w,y+h), (255, 0, 0), 2)
            print(x,y)

    #cv2.imshow('Motion Detector',imgContours)
    return imgContours

def preProcess(img):
    img=cv2.GaussianBlur(img,(5,5),5,0)
    img=cv2.Canny(img,50,100)
    kernel=np.ones((5,5),np.uint8)
    img=cv2.dilate(img,kernel)
    im=findcontours(img)
    # imcontour=img.copy()
    cv2.imshow("image",im)
    cv2.waitKey(0)
