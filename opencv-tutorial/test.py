# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np

src = cv.imread("C:/Users/lcx/Pictures/testimage/WindowsLogo.jpg")
src1 = cv.imread("C:/Users/lcx/Pictures/testimage/LinuxLogo.jpg")
# cv.namedWindow("input image", cv.WINDOW_NORMAL)
cv.imshow("input image", src)
# cv.namedWindow("input image2", cv.WINDOW_NORMAL)
cv.imshow("input image2",src1)
cv.waitKey(0)
cv.destroyAllWindows()