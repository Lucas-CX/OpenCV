# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


def add_demo(m1, m2):    # 两个大小相等的图像相加
    dst = cv.add(m1, m2)
    cv.imshow("add_demo", dst)


def subtract_demo(m1, m2):   # 相减
    dst = cv.subtract(m1, m2)
    cv.imshow("subtract_demo", dst)


def divide_demo(m1, m2):     # 相除
    dst = cv.divide(m1,  m2)
    cv.imshow("divde_demo", dst)


def multiply_demo(m1, m2):       # 相乘
    dst = cv.multiply(m1, m2)
    cv.imshow("multiply_demo", dst)


def others(m1, m2):
    M1, dev1 = cv.meanStdDev(m1)    # 求平均值和标准差，也可以用mean()函数直接求平均值
    M2, dev2 = cv.meanStdDev(m2)
    h, w = m1.shape[:2]       # 长和宽
    print(M1)
    print(M2)
    print(dev1)
    print(dev2)

    img = np.zeros([h, w], np.uint8)
    m, dev = cv.meanStdDev(img)
    cv.imshow("single", img)
    print (m)
    print(dev)


def logic_demo(m1, m2):      # 逻辑运算
    dst = cv.bitwise_and(m1,m2)
    # dst = cv.bitwise_or(m1,m2)
    # dst = cv.bitwise_not(m1)
    cv.imshow("logic_demo", dst)


def contrast_demo(image, c, b):
    h, w, ch = image.shape
    blank = np.zeros([h, w, ch], image.dtype)
    dst = cv.addWeighted(image, c, blank, 1-c, b)
    # 图像混合，c, 1-c为这两张图片的权重cv.addWeighted（）函数是进行线性加权的，其公式为：
    # alpha*src1 + beta*src2 + gamma，
    # 也可利用此函数进行调节对比度和亮度
    cv.imshow("con-bri-demo", dst)



print("***************Hello python***************")
src1 = cv.imread("C:/Users/lcx/Pictures/testimage/LinuxLogo.jpg")
src2 = cv.imread("C:/Users/lcx/Pictures/testimage/WindowsLogo.jpg")
src = cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
# cv.namedWindow("input image",cv.WINDOW_AUTOSIZE)

cv.imshow(" image1", src1)
cv.imshow(" image2", src2)
cv.imshow(" image", src)
logic_demo(src1, src2)

others(src1,src2)
contrast_demo(src, 1.2, 100)
cv.waitKey(0)
cv.destroyAllWindows()
