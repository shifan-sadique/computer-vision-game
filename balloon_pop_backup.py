import multiprocessing
import cvzone
import cv2
import numpy as np

from cvzone.ColorModule import ColorFinder
from multiprocessing import Process
import random
import time
# from detecthit import *

window_w=1280
window_h=720

class Balloon:
    def __init__(self,balloon):
        self.balloon=balloon
        self.h,self.w,_=balloon.shape






balloon1 = cv2.imread("images/new.png", cv2.IMREAD_UNCHANGED)
balloon1 = cv2.resize(balloon1, (0, 0), None, 0.5, 0.5)

balloon2 = cv2.imread("images/new1.png", cv2.IMREAD_UNCHANGED)
balloon2 = cv2.resize(balloon2, (0, 0), None, 0.5, 0.5)

balloonList=[]
balloonList.append(Balloon(balloon1))
balloonList.append(Balloon(balloon2))





pop = cv2.imread("images/pop.png", cv2.IMREAD_UNCHANGED)
pop = cv2.resize(pop, (0, 0), None, 0.1, 0.1)


backGroundImage=np.zeros((window_h,window_w,3),np.uint8)
backGroundImage.fill(255)


backgroudHeight, backgroudWidth, cb = backGroundImage.shape

balloonHeight=[]
balloonWidth=[]

for balloon in balloonList:
    balloonHeight.append(balloon.h) 
    balloonWidth.append(balloon.w) 

height_limit=[]
width_limit=[]

for i in range(len(balloonList)):
    height_limit.append(window_h-balloonHeight[i])
    width_limit.append(window_w-balloonWidth[i])


# add corresponidng elements of array
addArray=lambda first,second:[x + y for x, y in zip(first, second)]


# to check whether point in rect
def intersects(balloon, ball):
    
    bx,by,bw,bh= balloon[:]
    cx,cy= ball[:]
    idx=-1
    for i in range(len(bx)):
        if by[i]<cy and bh[i]>cy and bx[i]<cx and bw[i]>cx:
            idx=i
            break
    return idx
    
score=0
# proccess for game UI
def background(ball_bbox,ball_center):
    global score
    start=False
    while True:
        homeImage=backGroundImage.copy()
        cv2.putText( homeImage,"Press space  to start",(500, 500),cv2.FONT_HERSHEY_DUPLEX,1,(125, 246, 55),2)
        cv2.putText( homeImage,"Your score:"+str(score),(500, 600),cv2.FONT_HERSHEY_DUPLEX,1,(125, 246, 55),2)
        cv2.imshow("Backgroud", homeImage)
        key=cv2.waitKey(1)
        if key%256 == 32:
            start=True

            score=0
            yList=height_limit
            speed=[random.randint(2,4) for i in range(len(yList))]

            xList=[]
            TIMER=1000
            for idx in range(len(width_limit)):
                xList.append(random.randrange(0,width_limit[idx],step=70))
            print(xList)

        prevTime = time.time()
        popIndex=-1
        while start:
            curTime = time.time()
            if curTime-prevTime >= 1:
                prevTime = curTime
                TIMER = TIMER-1
            
            for idx in range(len(yList)):
                if yList[idx]<=1:
                    yList[idx]=height_limit[idx]
                    speed[idx]=random.randint(1,3)
                    xList[idx] =random.randrange(0,width_limit[idx],step=70)
            imgResult=backGroundImage.copy()
            
            for idx,y in enumerate(yList):
                if popIndex==idx:
                    imgResult = cvzone.overlayPNG(imgResult, pop, [popx,popy])
                else:
                    imgResult = cvzone.overlayPNG(imgResult, balloonList[idx].balloon, [xList[idx],y])
                
            yList = [y-speed[i] for i,y in enumerate(yList)]
    
            try:     
                cx,cy= ball_center[:]
            
                cv2.circle(imgResult, (cx,cy), radius=0, color=(0, 0, 255), thickness=10)
        
                popIndex=intersects([xList,yList,addArray(xList,balloonWidth),addArray(yList,balloonHeight)],[cx,cy])
                if popIndex>=0:
                    score=score+popIndex+1
                    # imgResult = cvzone.overlayPNG(imgResult, pop, [xList[idx],yList[idx]])
                    popx,popy=xList[popIndex],yList[popIndex]
                    yList[popIndex]=height_limit[popIndex]
                    speed[popIndex]=random.randint(1,3)
                    xList[popIndex] =random.randrange(0,width_limit[popIndex],step=70)
            except:
                pass                 
            cv2.putText( imgResult,"Score:"+str(score),(10, 30),cv2.FONT_HERSHEY_DUPLEX,1,(125, 246, 55),1)
            cv2.putText( imgResult,"Timer:"+str(TIMER),(400, 30),cv2.FONT_HERSHEY_DUPLEX,1,(125, 246, 55),1)    

            cv2.imshow("Backgroud", imgResult)
            if TIMER==0:
                start=False
                break
            if cv2.waitKey(2) & 0xFF == ord('q'):
                start=False
                break
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
# process for tracking ball
def ballTrack(ball_bbox,ball_center):
   
    cap = cv2.VideoCapture(2)
    # cap=cv2.flip(cap,1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_h)
    success, img = cap.read()
    h, w, _ = img.shape
    print("Webcam Dimension:",h, w, _)
    myColorFinder = ColorFinder(False)
    # hsvVals ={'hmin': 11, 'smin': 79, 'vmin': 63, 'hmax': 51, 'smax': 213, 'vmax': 223}
    # hsvVals ={'hmin': 148, 'smin': 104, 'vmin': 1, 'hmax': 163, 'smax': 231, 'vmax': 217}
    # hsvVals ={'hmin': 17, 'smin': 28, 'vmin': 186, 'hmax': 47, 'smax': 112, 'vmax': 255}
    # hsvVals ={'hmin': 8, 'smin': 88, 'vmin': 51, 'hmax': 25, 'smax': 255, 'vmax': 255}
    hsvVals={'hmin': 11, 'smin': 82, 'vmin': 75, 'hmax': 42, 'smax': 205, 'vmax': 192}


    while True:
        success, img = cap.read()
        
        # img=cv2.flip(img,1)
        imgColor, mask = myColorFinder.update(img, hsvVals)
        imgContour, contours = cvzone.findContours(img, mask)
       
        if contours:
            for i in range(0,4):
                ball_bbox[i]=contours[0]['bbox'][i]
            ball_center[0]=contours[0]['center'][0]
            ball_center[1]=contours[0]['center'][1]
        else:
            ball_bbox[0]=ball_bbox[1]=ball_bbox[2]=ball_bbox[3]=ball_center[0]=ball_center[1]=0

      
        cv2.imshow("Web Cam", imgContour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    ball_bbox = multiprocessing.Array("i",4)
    ball_center = multiprocessing.Array("i",2)
    Process(target=ballTrack,args=(ball_bbox,ball_center)).start()
    Process(target=background,args=(ball_bbox,ball_center)).start()
    print(ball_bbox[:])