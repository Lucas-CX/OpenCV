# -*- coding: utf-8 -*-

'''
一些图像知识：

1. 噪声：主要有三种：
椒盐噪声（Salt & Pepper）：含有随机出现的黑白亮度值。
脉冲噪声：只含有随机的正脉冲和负脉冲噪声。
高斯噪声：含有亮度服从高斯或正态分布的噪声。高斯噪声是很多传感器噪声的模型，如摄像机的电子干扰噪声。
2. 滤波器：主要两类：线性和非线性
线性滤波器：使用连续窗函数内像素加权和来实现滤波，同一模式的权重因子可以作用在每一个窗口内，即线性滤波器是空间不变的。

如果图像的不同部分使用不同的滤波权重因子，线性滤波器是空间可变的。因此可以使用卷积模板来实现滤波。
线性滤波器对去除高斯噪声有很好的效果。常用的线性滤波器有均值滤波器和高斯平滑滤波器。
(1) 均值滤波器：最简单均值滤波器是局部均值运算，即每一个像素只用其局部邻域内所有值的平均值来置换.
(2) 高斯平滑滤波器是一类根据高斯函数的形状来选择权值的线性滤波器。 高斯平滑滤波器对去除服从正态分布的噪声是很有效的。
非线性滤波器:
(1) 中值滤波器:均值滤波和高斯滤波运算主要问题是有可能模糊图像中尖锐不连续的部分。
中值滤波器的基本思想使用像素点邻域灰度值的中值来代替该像素点的灰度值，它可以去除脉冲噪声、椒盐噪声同时保留图像边缘细节。
中值滤波不依赖于邻域内与典型值差别很大的值，处理过程不进行加权运算。
中值滤波在一定条件下可以克服线性滤波器所造成的图像细节模糊，而对滤除脉冲干扰很有效。
(2) 边缘保持滤波器:由于均值滤波：平滑图像外还可能导致图像边缘模糊和中值滤波：去除脉冲噪声的同时可能将图像中的线条细节滤除。
边缘保持滤波器是在综合考虑了均值滤波器和中值滤波器的优缺点后发展起来的，它的特点是：
滤波器在除噪声脉冲的同时，又不至于使图像边缘十分模糊。
过程：分别计算[i，j]的左上角子邻域、左下角子邻域、右上角子邻域、右下角子邻域的灰度分布均匀度V；
然后取最小均匀度对应区域的均值作为该像素点的新灰度值。分布越均匀，均匀度V值越小。v=<(f(x, y) - f_(x, y))^2
'''


import cv2 as cv
import numpy as np


def blur_demo(image):           # 均值模糊
    dst = cv.blur(image, (1, 30))         # (1,30)卷积核大小为1*30
    cv.imshow("blur_demo", dst)


def median_blur_demo(image):           # 中值模糊
    dst = cv.medianBlur(image, 5)        # 中值模糊适合处理椒盐噪声
    cv.imshow("median_blur_demo", dst)


def custom_blur_demo(image):        # 自定义模糊
    # kernel = np.ones([5,5],np.float32)/25
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.float32)/9      # 锐化算子，卷积核模板
    # filter2D(src, ddepth(图像深度，-1表示默认和src一样深度), kernel, dst=None, anchor=None(锚点，卷积核中心), delta=None, borderType=None)
    dst = cv.filter2D(image, -1, kernel = kernel)
    cv.imshow("custom_blur_demo", dst)


print("***************Hello python***************")
src = cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
custom_blur_demo(src)
cv.waitKey(0)
cv.destroyAllWindows()
