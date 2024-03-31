# -*- coding:utf-8 -*-
import cv2 as cv
import numpy as np


def access_pixels(image):   # 自定义循环使像素取反
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    print("width:%s, height:%s, channels:%s"%(width, height, channels))
    for row in range(height):
        for col in range(width):
            for c in range(channels):
                pv = image[row, col, c]
                image[row, col, c] = 255-pv
    cv.imshow("pixels_demo", image)


def inverse(image):     # 像素取反 与 access_pixels(image)函数等价但运行效率更高
    dst = cv.bitwise_not(image)
    cv.imshow("inverse demo", dst)


def create_image():

    img1 = np.zeros([400, 400, 3], np.uint8)   # 多通道
    img1[:, :, 0] = np.ones([400, 400])*125
    cv.imshow("new image1", img1)
    img2=np.zeros([400, 400, 1], np.uint8)   # 单通道
    img2[:, :,  0] = np.ones([400, 400])*125
    cv.imshow("new image2", img2)
    img3 = np.ones([400, 400], np.uint8)     # 单通道,以一个二维数组赋值默认为单通道的，np.ones([400,400,1],np.uint8)也行
    img3 = img3*125
    cv.imshow("new image3", img3)

    m1 = np.ones([3, 3], np.uint8)
    m1.fill(1222.38)
    print(m1)
    m2 = m1.reshape([1, 9])
    print(m2)
    m3 = np.array([[2, 3, 4], [5, 6, 7], [4, 2, 1]], np.int32)
    m3.fill(9)
    print(m3)


print("************Hello python*************")
src = cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
t1 = cv.getTickCount()
inverse(src)
# access_pixels(src)
create_image()
t2 = cv.getTickCount()
print("time:%s ms" % ((t2-t1)*cv.getTickFrequency()*1000))
cv.waitKey(0)
cv.destroyAllWindows()
