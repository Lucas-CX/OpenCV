# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


def color_space_demo(image):  # 色彩空间的转换
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow("gray", gray)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    cv.imshow("hsv", hsv)
    yuv = cv.cvtColor(image, cv.COLOR_BGR2YUV)
    cv.imshow("yuv", yuv)
    # ycrcb = cv.cvtColor(image, cv.COLOR_BGR2YCrCb)
    # cv.imshow("ycrcb", ycrcb)   # python 2.x 的版本不支持 'ycrc'


def extrace_object_demo():
    capture = cv.VideoCapture("C:/Users/lcx/Pictures/testimage/demo4.mp4")
    while True:
        ret, frame = capture.read()

        if ret == False:
            break
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower_hsv = np.array([35, 43, 46])
        upper_hsv = np.array([77, 255, 255])                       # 提取绿色
        mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
        dst = cv.bitwise_and(frame, frame, mask=mask)      # 保留特征图像有颜色

        cv.imshow("video", frame)
        cv.imshow("mask", mask)
        cv.imshow("dst", dst)
        c = cv.waitKey(50)      # 可以控制视频播放的速率
        if c == 27:
            break


print("***************Hello python***************")
src = cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
# color_space_demo(src)
extrace_object_demo()


b, g, r = cv.split(src)       # 多通道的分离
cv.imshow("blue", b)
cv.imshow("green", g)
cv.imshow("red", r)

src[:, :, 0] = 0
cv.imshow("changed", src)
src = cv.merge([b, g, r])
cv.imshow("merged", src)


cv.waitKey(0)
cv.destroyAllWindows()
