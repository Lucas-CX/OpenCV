# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


def bi_demo(iamge):     # bilateralFilter(src, d, sigmaColor, sigmaSpace, dst=None, borderType=None)
    dst = cv.bilateralFilter(iamge, 0, 100, 15)    # 高斯双边
    cv.imshow("bi_demo", dst)
    """
       同时考虑空间与信息和灰度相似性，达到保边去噪的目的
       双边滤波的核函数是空间域核与像素范围域核的综合结果：
       在图像的平坦区域，像素值变化很小，对应的像素范围域权重接近于1，此时空间域权重起主要作用，相当于进行高斯模糊；
       在图像的边缘区域，像素值变化很大，像素范围域权重变大，从而保持了边缘的信息。
    """


def shift_demo(iamge):              # 均值迁移

    # pyrMeanShiftFiltering(src, sp, sr, dst=None, maxLevel=None, termcrit=None)
    # @param src The source 8-bit, 3-channel image.
    # @param dst The destination image of the same format and the same size as the source.
    # @param sp The spatial window radius.
    # @param sr The color window radius.
    # @param maxLevel Maximum level of the pyramid for the segmentation.
    # @param termcrit Termination criteria: when to stop meanshift iterations.

    dst = cv.pyrMeanShiftFiltering(iamge,10,50)
    cv.imshow("shift_demo",dst)
print("***************Hello python***************")
src=cv.imread("C:/Users/lcx/Pictures/testimage/lena.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
bi_demo(src)
shift_demo(src)
cv.waitKey(0)
cv.destroyAllWindows()
