# import necessary libraries

import cv2
import numpy as np

# Turn on Laptop's webcam
cap = cv2.VideoCapture(1) 
width=1280
height=720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def nothing(x):
    pass
 
# Creating a window with black image

# cv2.namedWindow('image')
 
# creating trackbars for red color change
# cv2.createTrackbar('x1', 'image', 0, width, nothing)
# cv2.createTrackbar('y1', 'image', 0, height, nothing)
# cv2.createTrackbar('x2', 'image', 0, width, nothing)
# cv2.createTrackbar('y2', 'image', 0, height, nothing)
 
# cv2.createTrackbar('x3', 'image', 0, width, nothing)
# cv2.createTrackbar('y3', 'image', 0, height, nothing)
 
# cv2.createTrackbar('x4', 'image', 0, width, nothing)
# cv2.createTrackbar('y4', 'image', 0, height, nothing)
 
click_no=1
x1,y1,x2,y2,x3,y3,x4,y4=0,0,0,0,0,0,0,0
def click_event(event, x, y, flags, params):
    global click_no
    global x1,y1,x2,y2,x3,y3,x4,y4
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        if click_no == 1:
            x1,y1=x,y
            click_no=click_no+1
        elif click_no==2:
            x2,y2=x,y
            click_no=click_no+1
        elif click_no==3:
            x3,y3=x,y
            click_no=click_no+1
        elif click_no==4:
            x4,y4=x,y
            click_no=click_no+1
            np.save("pers_values.npy",np.array([[x1, y1], [x2, y2],	[x3, y3], [x4, y4]]))
        # displaying the coordinates
        # on the image window
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(frame, str(x) + ',' +
        #             str(y), (x,y), font,
        #             1, (255, 0, 0), 2)
        # cv2.imshow('image', frame)
 
    

while True:
    
    ret, frame = cap.read()
    # cv2.imwrite("sample.png",frame)
    # frame=cv2.imread("sample.png")
   

    cv2.circle(frame, (x1,y1), radius=5, color=(0, 0, 255), thickness=-1)
    cv2.circle(frame, (x2,y2), radius=5, color=(33, 35, 100), thickness=-1)
    cv2.circle(frame, (x3,y3), radius=5, color=(44, 235, 33), thickness=-1)
    cv2.circle(frame, (x4,y4), radius=5, color=(235, 226, 33), thickness=-1)
    pts1 = np.float32([[x1, y1], [x2, y2],	[x3, y3], [x4, y4]])
    # pts1 = np.float32([[287, 113], [475, 121],	[282, 256], [475, 255]])
    pts2 = np.float32([[0, 0], [width, 0],[0, height], [width, height]])
    
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (width, height))
 
    # Wrap the transformed image
    cv2.imshow('frame', frame) # Initial Capture
    cv2.imshow('frame1', result) # Transformed Capture
    cv2.setMouseCallback('frame', click_event)

    if cv2.waitKey(24) == 27:
        break

cap.release()
cv2.destroyAllWindows()
