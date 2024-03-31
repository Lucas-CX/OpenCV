# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
from  matplotlib import pyplot as plt
'''
这里先解释直方图（histogram）是什么？
直方图是为了表明数据分布情况。通俗地说就是哪一块数据所占比例或者出现次数较高，哪一块出现概率低。
'''



def plot_demo(image):
    plt.hist(image.ravel(),256,[0,256])     #image.ravel（）多维数组转换为一维数组的功能
    plt.show("直方图")

'''
plt.hist()参数解释  hist(x, bins=None, range=None, density=None, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color=None, label=None, stacked=False, normed=None, hold=None, data=None, **kwargs)

x : (n,) array or sequence of (n,) arrays
这个参数是指定每个bin(箱子)分布的数据,对应x轴
bins : integer or array_like, optional
这个参数指定bin(箱子)的个数,也就是总共有几条条状图
normed : boolean, optional
If True, the first element of the return tuple will be the counts normalized to form a probability density, i.e.,n/(len(x)`dbin)
这个参数指定密度,也就是每个条状图的占比例比,默认为1
color : color or array_like of colors or None, optional
这个指定条状图的颜色
'''


def image_hist(image):      #画三通道的直方图
    color = ('blue','green','red')      #画笔颜色的值可以为大写或小写或只写首字母或大小写混合
    for i,color in enumerate(color):
        hist = cv.calcHist([image],[i],None,[256],[0,256])
        '''
       calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
        images参数表示输入图像，传入时应该用中括号[]括起来
        channels参数表示传入图像的通道，如果是灰度图像，那就不用说了，只有一个通道，值为0，如果是彩色图像（有3个通道），那么值为0, 1, 2, 中选择一个，对应着BGR各个通道。这个值也得用[]
        传入。
        mask参数表示掩膜图像。如果统计整幅图，那么为None。主要是如果要统计部分图的直方图，就得构造相应的掩膜来计算。
        histSize参数表示灰度级的个数，需要中括号，比如[256]
        ranges参数表示像素值的范围，通常[0, 256]。此外，假如channels为[0, 1], ranges为[0, 256, 0, 180], 则代表0通道范围是0 - 256, 1通道范围0 - 180。
        hist参数表示计算出来的直方图。
    '''


        plt.plot(hist,color = color)        #画图函数
        plt.xlim([0,256])       #设置x轴的范围
    plt.show()

'''
# 设置x轴的取值范围为：-1到2
plt.xlim(-1, 2)
# 设置y轴的取值范围为：-1到3
plt.ylim(-1, 3)
# 设置x轴的文本，用于描述x轴代表的是什么
plt.xlabel("I am x")
# 设置y轴的文本，用于描述y轴代表的是什么
plt.ylabel("I am y")
plt.plot(x, y2)
# 绘制红色的线宽为1虚线的线条
plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--')
# 显示图表
plt.show()
'''





print("***************Hello python***************")
src=cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
plot_demo(src)
image_hist(src)
cv.waitKey(0)
cv.destroyAllWindows()