import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt



'''
反向投影查找原理：查找的方式就是不断的在输入图像中切割跟模板图像大小一致的图像块，并用直方图对比的方式与模板图像进行比较。
假设我们有一张100x100的输入图像，有一张10x10的模板图像，查找的过程是这样的：
（1）从输入图像的左上角(0,0)开始，切割一块(0,0)至(10,10)的临时图像；
（2）生成临时图像的直方图；
（3）用临时图像的直方图和模板图像的直方图对比，对比结果记为c；
（4）直方图对比结果c，就是结果图像(0,0)处的像素值；
（5）切割输入图像从(0,1)至(10,11)的临时图像，对比直方图，并记录到结果图像；
（6）重复（1）～（5）步直到输入图像的右下角。
3.反向投影的结果包含了：以每个输入图像像素点为起点的直方图对比结果。可以把它看成是一个二维的浮点型数组，二维矩阵，或者单通道的浮点型图像。
'''
def back_projection_demo():
    sample = cv.imread("C:/Users/lcx/Pictures/testimage/zlyhead.png")
    target = cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
    roi_hsv = cv.cvtColor(sample,cv.COLOR_BGR2HSV )
    target_hsv = cv.cvtColor(target,cv.COLOR_BGR2HSV)

    # show image
    cv.imshow("sample",sample)
    cv.imshow("target",target)

    roiHist = cv.calcHist([roi_hsv],[0,1],None,[32,32],[0,180,0,256])       #形成二值直方图
    #进行归一化#normalize是归一化函数第一个参数是输入图象，第二个参数是输出图像然后再是输出结果的最小值，最大值。然后值归一化类型
    cv.normalize(roiHist ,roiHist,0,255,cv.NORM_MINMAX)
    dst = cv.calcBackProject([target_hsv],[0,1],roiHist,[0,180,0,156],1)
    cv.imshow("backprojectDemo",dst)



def hist2d_demo(image):
    hsv = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    hist = cv.calcHist([image],[0,1],None,[32,32],[0,180,0,256])
    #cv.imshow("hist2d",hist)
    plt.imshow(hist,interpolation='nearest')
    plt.title("2D Histogram")


print("***************Hello python***************")
src=cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image",cv.WINDOW_AUTOSIZE)
cv.imshow("input image",src)

hist2d_demo(src)
#back_projection_demo()
cv.waitKey(0)
cv.destroyAllWindows()