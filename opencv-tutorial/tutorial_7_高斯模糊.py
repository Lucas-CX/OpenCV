# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


def clamp(pv):
    if pv > 255:
        return 255
    if pv < 0:
        return 0
    else:
        return pv


def gaussian_noise(image):          # 给图片添加高斯噪声
    h,w,c = image.shape
    for row in range(h):
        for col in range(w):
            s = np.random.normal(0,20,3)
            b = image[row,col,0]
            g = image[row,col,1]
            r = image[row,col,2]
            image[row, col, 0] = clamp(b + s[0])
            image[row, col, 1] = clamp(g + s[0])
            image[row, col, 2] = clamp(r + s[0])
    cv.imshow("noise image", image)


print("***************Hello python***************")
src=cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
t1 = cv.getTickCount()
gaussian_noise(src)
t2 = cv.getTickCount()
time = (t2-t1)/cv.getTickFrequency()
print("time consume : %s"%(time*1000))

# GaussianBlur(src, ksize , sigmaX, dst=None, sigmaY=None, borderType=None)
# ksize表示卷积核大小，sigmaX，Y表示x，y方向上的标准差，这两者只需一个即可，并且ksize为大于0的奇数
dst = cv.GaussianBlur(src,(5,5),0)      # 轻微模糊用（3，3）
cv.imshow("Gaussian Blur",dst)
cv.waitKey(0)
cv.destroyAllWindows()
