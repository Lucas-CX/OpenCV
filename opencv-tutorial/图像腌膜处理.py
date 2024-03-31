# -*- coding: utf-8 -*-
import cv2
import numpy as np
"""
说明：所用图像没有选好，效果不是很好，但已体现mask的作用
"""


# 加载图像
print(cv2.useOptimized())
img1 = cv2.imread('C:/Users/lcx/Desktop/messi5.jpg')
img2 = cv2.imread('C:/Users/lcx/Desktop/WindowsLogo.jpg')
rows,cols,channels = img2.shape
roi = img1[0:rows, 0:cols ]
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray,100, 255, cv2.THRESH_BINARY)     # 函数返回的ret为阈值，mask为二值化后的图像
mask_inv = cv2.bitwise_not(mask)

img1_bg = cv2.bitwise_and(roi,roi, mask = mask)

img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)
dst = cv2.add(img1_bg,img2_fg)
cv2.imshow("img_add",dst)
cv2.imshow("img2_fg",img2_fg )
cv2.imshow("img1_bg",img1_bg)
cv2.imshow("mask_inv",mask_inv)
cv2.imshow("mask",mask)
cv2.imshow("img2gray",img2gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
