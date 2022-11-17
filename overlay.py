import multiprocessing
import cvzone
import cv2
import numpy as np
import old.balloonhit as balloonhit
from cvzone.ColorModule import ColorFinder
from multiprocessing import Process, Queue
# from detecthit import *

window_w=1280
window_h=720



# cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_w)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_h)
# success, img = cap.read()



blue = cv2.imread("images/new.png", cv2.IMREAD_UNCHANGED)
blue = cv2.resize(blue, (0, 0), None, 0.2, 0.2)
pop = cv2.imread("images/pop.png", cv2.IMREAD_UNCHANGED)
pop = cv2.resize(pop, (0, 0), None, 0.1, 0.1)


img=np.zeros((window_h,window_w,3),np.uint8)
img.fill(255)
hf, wf, cf = blue.shape
hb, wb, cb = img.shape




height_limit=window_h-hf
width_limit=window_h-wf

print(blue.shape,"---------------------")
print(img.shape,"---------------------")
print("Height limit",height_limit)
print("Width limit",width_limit)

def intersects(balloon, ball):
    # return 
    # pass
    bx,by,bw,bh= balloon[:]
    cx,cy= ball[:]
    # print(by<cy , (bh)>cy , bx<cx , (bw)>cx)
    return by<cy and (bh)>cy and bx<cx and (bw)>cx
    

def background(ball_bbox,ball_center):
    score=0
    y=height_limit
    x=0
    while True:
        if y==0:
            y=height_limit
     
        imgResult = cvzone.overlayPNG(img, blue, [x,y])
        y=y-1
        if y%5==0 and x<width_limit:
            x=x+2
        if x>=width_limit:
            x=0
  
        try:
      
            # bx,by,bw,bh= ball_bbox[:]
            cx,cy= ball_center[:]
         
            # cv2.rectangle(imgResult,(bx,by) , (bx+bw,by+bh),
            #             (255, 0, 0), 2)
            cv2.circle(imgResult, (cx,cy), radius=0, color=(0, 0, 255), thickness=3)
            # print([x,y,x+wf,y+hf],[cx,cy])
            if intersects([x,y,x+wf,y+hf],[cx,cy]):
                score=score+1
                y=height_limit
                x=x+20
        except:
            pass
        cv2.rectangle(imgResult,(x,y) , (x+wf,y+hf),
                        (255, 0, 0), 1)
        # print(ball_bbox[:])
        cv2.putText( imgResult,"Score:"+str(score),(10, 30),cv2.FONT_HERSHEY_DUPLEX,1,(125, 246, 55),1)
        # imgBalloon=balloonhit.preProcess(canny)
        # cv2.imshow("canny",imgBalloon)
        cv2.imshow("Backgroud", imgResult)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

def ballTrack(ball_bbox,ball_center):
   
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_h)
    success, img = cap.read()
    h, w, _ = img.shape
    
    myColorFinder = ColorFinder(False)
    hsvVals ={'hmin': 11, 'smin': 79, 'vmin': 63, 'hmax': 51, 'smax': 213, 'vmax': 223}
    image=cv2.imread("ball_yellow.jpg")

    while True:
        success, img = cap.read()
        # img = image
        img=cv2.flip(img,1)
        imgColor, mask = myColorFinder.update(img, hsvVals)
        imgContour, contours = cvzone.findContours(img, mask)
        # print(contours)
        if contours:
            for i in range(0,4):
                ball_bbox[i]=contours[0]['bbox'][i]
            ball_center[0]=contours[0]['center'][0]
            ball_center[1]=contours[0]['center'][1]
        else:
            ball_bbox[0]=ball_bbox[1]=ball_bbox[2]=ball_bbox[3]=ball_center[0]=ball_center[1]=0

        # imgStack = cvzone.stackImages([img, imgColor], 2, 0.5)
        # cv2.imshow("Image", imgStack)
        # imgContour = cv2.resize(imgContour, (0, 0), None, 0.5, 0.5)
        cv2.imshow("Web Cam", imgContour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    ball_bbox = multiprocessing.Array("i",4)
    ball_center = multiprocessing.Array("i",2)
    Process(target=background,args=(ball_bbox,ball_center)).start()
    Process(target=ballTrack,args=(ball_bbox,ball_center)).start()
    print(ball_bbox[:])