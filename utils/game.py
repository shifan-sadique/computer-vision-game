import cv2
import numpy as np
import cvzone


# balloon=cv2.imread("blue1.png",cv2.IMREAD_UNCHANGED)
# balloon=balloon[:500][:][:]
# print(balloon.shape)
# cv2.imwrite("new.png",balloon)

balloon=cv2.imread("balloon_violet.png",cv2.IMREAD_UNCHANGED)
print(balloon.shape)
balloon = cv2.resize(balloon, (0, 0), None, 0.5, 0.5)
# balloon=balloon[:500][:][:]
print(balloon.shape)
cv2.imwrite("new1.png",balloon)