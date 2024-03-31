# _*_ coding: utf-8 _*_
import cv2
import numpy
img = cv2.imread("C:/Users/lcx/Pictures/testimage/opencv-logo-white.png")
print(img.shape)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (50, 20), font, 1, (255, 255, 255), 2)
'''
• 你要绘制的文字 
• 你要绘制的位置 
•字体类型（通过查看 cv2.putText() 的文档找到支持的字体） 
• 字体的大小 
•文字的一般属性如颜色，粗细，线条的类型等。为了更好看一点推荐使用 linetype=cv2.LINE_AA
'''
winname = 'example'
cv2.namedWindow(winname)
cv2.imshow(winname, img)
cv2.waitKey(0)
cv2.destroyWindow(winname)


