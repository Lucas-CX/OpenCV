

import cv2 as cv
import numpy as np


def equalHist_demo(image):      # 全局直方图均衡化，用于增强图像对比度，即黑的更黑，白的更白
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    dst = cv.equalizeHist(gray)
    cv.imshow("equalHist_demo",dst)


def clahe_demo(image):      # 局部直方图均衡化
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    clahe = cv.createCLAHE(clipLimit=5.0,tileGridSize=(8,8))
    '''
    用于生成自适应均衡化图像
    参数说明：clipLimit颜色对比度的阈值， titleGridSize进行像素均衡化的网格大小，即在多少网格下进行直方图的均衡化操作
    直方图均衡化：一般可以用来提升图片的亮度，频数均衡化指的是让频数的分布看起来更加均匀一些
    '''
    dst = clahe.apply(gray)
    cv.imshow("clahe_demo",dst)

    # 创建直方图


def create_rgb_hist(image):
    h, w, c = image.shape
    rgbHist = np.zeros([16*16*16,1],np.float32)
    bsize = 256/16
    for row in range(h):
        for col in range(w):
            b = image[row,col,0]
            g = image[row,col,1]
            r = image[row,col,2]
            index = np.int(b/bsize)*16*16+np.int(g/bsize)*16+np.int(r/bsize)        # ???????
            rgbHist[np.int(index),0] = rgbHist[np.int(index),0]+1                # ???????
    return rgbHist


# 利用直方图比较相似性，用巴氏和相关性比较好
def hist_compare(image1,image2):
    hist1 = create_rgb_hist(image1)
    hist2 = create_rgb_hist(image2)
    match2 = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)
    match1 = cv.compareHist(hist1, hist2, cv.HISTCMP_BHATTACHARYYA)
    match3 = cv.compareHist(hist1, hist2, cv.HISTCMP_CHISQR)
    print("巴氏距离：%s, 相关性：%s, 卡方：%s"%(match1,match2,match3))



print("***************Hello python***************")
src=cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image",cv.WINDOW_AUTOSIZE)
cv.imshow("input image",src)
equalHist_demo(src)
# clahe_demo(src)
image1 = cv.imread("C:/Users/lcx/Pictures/testimage/rice.png")
image2 = cv.imread("C:/Users/lcx/Pictures/testimage/noise_rice.png")
cv.imshow("image1",image1)
cv.imshow("image2",image2)
hist_compare(image1,image2)

cv.waitKey(0)
cv.destroyAllWindows()