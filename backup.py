import multiprocessing
import cvzone
import cv2
import numpy as np
import old.balloonhit as balloonhit
from cvzone.ColorModule import ColorFinder
from multiprocessing import Process
import random
# from detecthit import *

window_w=1280
window_h=720

class Balloon:
    def __init__(self,balloon):
        self.balloon=balloon
        self.h,self.w,_=balloon.shape


# cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_w)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_h)
# success, img = cap.read()



balloon1 = cv2.imread("images/new.png", cv2.IMREAD_UNCHANGED)
balloon1 = cv2.resize(balloon1, (0, 0), None, 0.2, 0.2)

balloon2 = cv2.imread("images/new1.png", cv2.IMREAD_UNCHANGED)
# blue1=cv2.cvtColor(blue1,cv2.COLOR_BGR2HSV )
balloon2 = cv2.resize(balloon2, (0, 0), None, 0.2, 0.2)

balloonList=[]
balloonList.append(Balloon(balloon1))
balloonList.append(Balloon(balloon1))
balloonList.append(Balloon(balloon2))
# balloonList.append(Balloon(blue))



pop = cv2.imread("images/pop.png", cv2.IMREAD_UNCHANGED)
pop = cv2.resize(pop, (0, 0), None, 0.1, 0.1)


backGround=np.zeros((window_h,window_w,3),np.uint8)
backGround.fill(255)


backgroudHeight, backgroudWidth, cb = backGround.shape

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


addArray=lambda first,second:[x + y for x, y in zip(first, second)]



def intersects(balloon, ball):
    
    bx,by,bw,bh= balloon[:]
    cx,cy= ball[:]
    idx=-1
    for i in range(len(bx)):
        if by[i]<cy and bh[i]>cy and bx[i]<cx and bw[i]>cx:
            idx=i
            break
    return idx
    

def background(ball_bbox,ball_center):
  
    

        score=0
        yList=height_limit
        speed=[random.randint(2,4) for i in range(len(yList))]

        xList=[]
        print(width_limit)
        for idx in range(len(width_limit)):
            xList.append(random.randrange(0,width_limit[idx],step=70))
        print(xList)
    
        while True:
            
            for idx in range(len(yList)):
                if yList[idx]<=1:
                    yList[idx]=height_limit[idx]
                    speed[idx]=random.randint(1,3)
                    xList[idx] =random.randrange(0,width_limit[idx],step=70)
            imgResult=backGround.copy()
            for idx,y in enumerate(yList):
                imgResult = cvzone.overlayPNG(imgResult, balloonList[idx].balloon, [xList[idx],y])
            yList = [y-speed[i] for i,y in enumerate(yList)]
    
            # for idx in range(len(yList)):    
            #     if yList[idx]%5==0 and xList[idx]<width_limit[idx]:
            #         xList[idx]=xList[idx]+2
            #     if xList[idx]>=width_limit[idx]:
            #         xList[idx]=random.randrange(0,width_limit[idx],step=70)
    
            try:
        
                bx,by,bw,bh= ball_bbox[:]
                cx,cy= ball_center[:]
            
                # cv2.rectangle(imgResult,(bx,by) , (bx+bw,by+bh),
                #             (255, 0, 0), 2)
                cv2.circle(imgResult, (cx,cy), radius=0, color=(0, 0, 255), thickness=3)
        
                idx=intersects([xList,yList,addArray(xList,balloonWidth),addArray(yList,balloonHeight)],[cx,cy])
                if idx>=0:
                    score=score+1
                    yList[idx]=height_limit[idx]
                    speed[idx]=random.randint(1,3)
                    xList[idx] =random.randrange(0,width_limit[idx],step=70)
            except:
                pass
  
            
            cv2.putText( imgResult,"Score:"+str(score),(10, 30),cv2.FONT_HERSHEY_DUPLEX,1,(125, 246, 55),1)
        
            cv2.imshow("Backgroud", imgResult)
            if cv2.waitKey(2) & 0xFF == ord('q'):
               
                break

def ballTrack(ball_bbox,ball_center):
   
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_h)
    success, img = cap.read()
    h, w, _ = img.shape
    print("Webcam Dimension:",h, w, _)
    myColorFinder = ColorFinder(False)
    # hsvVals ={'hmin': 11, 'smin': 79, 'vmin': 63, 'hmax': 51, 'smax': 213, 'vmax': 223}
    hsvVals ={'hmin': 148, 'smin': 104, 'vmin': 1, 'hmax': 163, 'smax': 231, 'vmax': 217}
    while True:
        success, img = cap.read()
       
        img=cv2.flip(img,1)
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
    Process(target=background,args=(ball_bbox,ball_center)).start()
    Process(target=ballTrack,args=(ball_bbox,ball_center)).start()
    print(ball_bbox[:])