# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np




def get_image_info(image):
    print(type(image))
    print(image.shape)
    print(image.dtype)
    pixel_data = np.array(image)
    print(pixel_data)


def video_demo():
    capture = cv.VideoCapture(0)
    while (True):
        ret, frame = capture.read()
        frame = cv.flip(frame, 1)
        cv.imshow("video", frame)
        c = cv.waitKey(50)
        if c == 27:
            break


print("*******************Hello python*********************")
src = cv.imread("C:/Users/lcx/Pictures/testimage/zly.jpg")
cv.namedWindow("input image", cv.WINDOW_NORMAL)     # 第二个参数不填默认是cv.WINDOW_AUTOSIZE,我们填的这个参数是可以调整大小的
cv.imshow("input image", src)
get_image_info(src)
video_demo()
gray=cv.cvtColor(src,cv.COLOR_BGR2GRAY)
cv.imwrite("C:/Users/lcx/Desktop/result.png",gray)
cv.waitKey(0)
cv.destroyAllWindows()  # 加参数可以指定销毁那个窗口
