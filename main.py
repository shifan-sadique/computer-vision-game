# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
from cgi import test
from multiprocessing.connection import wait


# Press the green button in the gutter to run the script.
import balloonhit
from detecthit import *
import interface
import cv2

if __name__ == '__main__':
    #interface.set_screen()
    #balloonhit.detectscreen()
    img=cv2.imread("ball1.png")
    imgBalloon,bbox=findballoons(img)
    img=detectHit(img,bbox)
    cv2.imshow("imageshow",img)
    cv2.waitKey(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
