# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

print("***************Hello python***************")
src=cv.imread("C:/Users/lcx/Desktop/testimage/thumb-5.png")
dst = cv.cvtColor(src, cv.COLOR_BGR2HSV)  # BGR转HSV

cv.namedWindow("input image",cv.WINDOW_AUTOSIZE)
cv.imshow("input image",src)

mask1 = cv.inRange(dst, np.array([0, 43, 46,]),np.array([10, 255, 255]))
mask2 = cv.inRange(dst, np.array([156, 43, 46,]),np.array([180, 255, 255]))
cv.imshow("mask11",mask1)
cv.imshow("mask21",mask2)
mask_add = cv.addWeighted(mask1,1,mask2,1,0)
cv.imshow('mask_add1',mask_add)
kernel = np.ones((5,5),np.float32)/25
dst = cv.filter2D(mask_add,-1,kernel)
cv.imshow("dst",dst)
ret, mask = cv.threshold(dst,230, 255, cv.THRESH_BINARY_INV)
cv.imshow("mask",mask)


#cv.imshow("mask1",mask1)
#cv.imshow("mask2",mask2)
cv.waitKey(0)
cv.destroyAllWindows()