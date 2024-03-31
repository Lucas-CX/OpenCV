# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


'''
漫水填充：就是将与种子点相连接的区域换成特定的颜色，通过设置连通方式或像素的范围可以控制填充的效果。
通常是用来标记或分离图像的一部分对其进行处理或分析，或者通过掩码来加速处理过程。可以只处理掩码指定的部分或者对掩码上的区域进行屏蔽不处理。
主要作用就是：选出与种子点连通的且颜色相近的点，对像素点的值进行处理。如果遇到掩码，根据掩码进行处理。
工作流程：
选定种子点（x,y）
检查种子点的颜色，如果该点颜色与周围连接点的颜色不相同，则将周围点颜色设置为该点颜色，如果相同则不做处理。但是周围点不一定都会变成和种子点的颜色相同，
如果周围连接点在给定的范围内(lodiff - updiff)内或在种子点的象素范围内才会改变颜色。
检测其他连接点，进行2步骤的处理，直到没有连接点，即到达检测区域边界停止。

Iimage:输入图像，可以是一通道或者是三通道。
mask:   该版本特有的掩膜。 单通道，8位，在长宽上都比原图像image多2个像素点。另外，当flag为FLOORFILL_MAK_ONLY时，只会填充mask中数值为0的区域。
seedPoint:  漫水填充的种子点，即起始点。
newVal: 被填充的像素点新的像素值
loDiff： 表示当前的观察点像素值与其相邻区域像素值或待加入该区域的像素之间的亮度或颜色之间负差的最大值。
upDiff: 表示当前的观察点像素值与其相邻区域像素值或待加入该区域的像素之间的亮度或颜色之间负差的最小值。
flag：   当为CV_FLOODFILL_FIXED_RANGE 时，待处理的像素点与种子点作比较，在范围之内，则填充此像素 。（改变图像）
CV_FLOODFILL_MASK_ONLY 此位设置填充的对像， 若设置此位，则mask不能为空，此时，函数不填充原始图像img，而是填充掩码图像.
--------------------- 
原文：https://blog.csdn.net/weixin_42508025/article/details/84029054 
'''


def fill_color_demo(image):     # cv.FLOODFILL_FIXED_RANGE泛洪填充
    copyimg = image.copy()
    h, w = image.shape[:2]
    mask = np.zeros([h+2, w+2], np.uint8)
    cv.floodFill(copyimg, mask, (30, 30), (0, 255, 255), (100, 100, 100), (50, 50, 50), cv.FLOODFILL_FIXED_RANGE)
    cv.imshow("fill_color_demo", copyimg)


def fill_binary_demo(image):   # cv.FLOODFILL_MASK_ONLY图像泛洪填充,在python2.x环境下跑不通,可能用法有区别
    image = np.zeros([400, 400, 3], np.uint8)
    image[100:300, 100:3000, :] = 255
    cv.imshow("fill_binary_demo", image)

    mask = np.ones([402, 402, 1], np.uint8)
    mask[101:301, 101:301] = 0
    cv.floodFill(image, mask, (200, 200), (0, 0, 255), cv.FLOODFILL_MASK_ONLY)
    cv.imshow("filled binary", image)


print("***************Hello python***************")
src=cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
fill_binary_demo(src)


face = src[100:350, 250:450]
gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)          # 该函数返回的gray是单通道的
backface = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)      # backface是被赋值的3通道的，这个函数的作用是为了下面的赋值操作，图片还是灰度的图片

src[100:350, 250:450] = backface                     # 同类型的可以进行赋值

cv.imshow("face", face)
cv.imshow("backface", backface)
cv.imshow("facechangeim", src)

fill_color_demo(src)


cv.waitKey(0)
cv.destroyAllWindows()
