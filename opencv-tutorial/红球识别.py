# -*- coding:utf-8 -*-
# author:fanzhe Edition:6.0
# robot video edition

import numpy as np
import argparse
import cv2
import cv2.cv as cv
from naoqi import ALProxy
import vision_definitions
import math

hsv_low = np.array([0, 0, 0]) # 初始化
hsv_high = np.array([255, 255, 255])

def Circle_dec(red_fit, image):
    '''
    Detect Redball and return the position
    :param image: must be a Cv2_iamge
    :return:Position infomation
    '''
    # smooth
    kernel = np.ones((3,3),np.float32)/25
    # kernel = np.ones((3, 3), np.float32) / 30
    for i in range(3):
        fit = cv2.filter2D(red_fit, -1, kernel)

    # add_weight
    cv2.addWeighted(fit, 255, fit, 0, 0, fit)

    try:
        circles1 = cv2.HoughCircles(fit, cv.CV_HOUGH_GRADIENT, 1, 2000,param1=100, param2=10, minRadius=1, maxRadius=30)
        circles = circles1[0, :, :]
        circles = np.uint16(np.around(circles))
        if circles[0][2] < 500:
            for i in circles[:]:
                # cv2.circle(image, (i[0], i[1]), i[2], (255, 0, 0), 3)
                cv2.circle(image, (i[0], i[1]), 2, (255, 0, 255), 5)
                # print "圆心坐标: {},{}".format(i[0], i[1])
    except:
        pass
        # 用于没有找到球的报错

    return image,fit


def Green(image, green):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_low_g = np.array(green[0])
    hsv_high_g = np.array(green[1])

    # hsv_low = np.array([47, 96, 22])
    # hsv_high = np.array([255, 0, 255])
    mask = cv2.inRange(hsv, hsv_low_g, hsv_high_g)
    black = cv2.medianBlur(mask, 9)
    contours, hierarchy = cv2.findContours(black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c_max = []
    max_area = 0
    max_cnt = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_cnt = cnt

    if str(type(max_cnt)) == '<type \'numpy.ndarray\'>':
        c_max.append(max_cnt)
    if len(c_max):
        cv2.drawContours(black, c_max, -1, (255, 255, 255), thickness=-1)
    res = cv2.bitwise_and(image, image, mask=black)

    # cv2.imshow("black", black)
    # cv2.imshow("res", res)
    # cv2.imshow("mask", mask)
    return res

def Stitch_imagesh(image_1, image_2):
    hmerge = np.hstack((image_1, image_2))
    return hmerge

def Stitch_imagesw(image_1, image_2):
    wmerge = np.vstack((image_1, image_2))
    return  wmerge

def ChangeIm(img):
    '''
    Change Cv_image to Cv2_image
    :param img: must be cv_image
    :return: cv2_image
    '''
    cv_mat = img[:]
    result = np.asarray(cv_mat)
    return result

def Stand_up(IP):
    motionProxy = ALProxy("ALMotion", IP, 9559)
    postureProxy = ALProxy("ALRobotPosture", IP, 9559)
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.moveInit()
    motionProxy.setAngles('HeadPitch', -5 * math.pi / 180.0, 0.8)

def analyse(green_data):
    '''
    将文本形式的数据改为数组
    :param green_data: str '*.*.*.*.*.*'
    :return: [[*],[*]]
    '''
    str_list = green_data.split('.')
    temp = []
    for i in str_list:
        temp.append(int(i))
    temp = [temp[:3],temp[3:]]
    return temp

def Connect(green,Ip='127.0.0.1',Port=9559,  Mod=0, Cont=65, Loop=True, CameraId=0, fps=30):
    '''
    主代码
    :param Ip:机器人的链接ip
    :param Mod: 默认模式是找红球 0 ；找杆模式是 1
    :param Cont: 找黄杆的相关参数
    :param Loop: 是否循环查找
    :param Port: 机器人端口
    :param CameraId: 默认使用
    :param fps:
    :param green: 绿色背景的过滤信息
    :return:
    '''

    resolution = vision_definitions.kQVGA  # 320 * 240
    colorSpace = vision_definitions.kBGRColorSpace
    image_cv = cv.CreateImageHeader((320, 240), cv.IPL_DEPTH_8U, 3)
    videoProxy = ALProxy("ALVideoDevice", Ip, Port)
    imgClient = videoProxy.subscribeCamera("OpenCV_Client", CameraId, resolution, colorSpace, fps)

    def Relax_Camare(imgClinet):
        if imgClinet != "":
            videoProxy.unsubscribe(imgClient)
    try:

        def h_low(value):
            hsv_low[0] = value

        def h_high(value):
            hsv_high[0] = value

        def s_low(value):
            hsv_low[1] = value

        def s_high(value):
            hsv_high[1] = value

        def v_low(value):
            hsv_low[2] = value

        def v_high(value):
            hsv_high[2] = value

        cv2.namedWindow('V6.0 by:fanzhe',1)
        cv2.resizeWindow('V6.0 by:fanzhe', 320, 300)
        cv2.createTrackbar('H min', 'V6.0 by:fanzhe', 0, 180, h_low)
        cv2.createTrackbar('H max', 'V6.0 by:fanzhe', 0, 180, h_high)
        cv2.createTrackbar('S min', 'V6.0 by:fanzhe', 0, 255, s_low)
        cv2.createTrackbar('S max', 'V6.0 by:fanzhe', 0, 255, s_high)
        cv2.createTrackbar('V min', 'V6.0 by:fanzhe', 0, 255, v_low)
        cv2.createTrackbar('V max', 'V6.0 by:fanzhe', 0, 255, v_high)

        while Loop:
            imageData = videoProxy.getImageRemote(imgClient)
            cv.SetData(image_cv, imageData[6])
            image_cv2 = ChangeIm(image_cv)
            image_1 = image_cv2.copy()
            image_2 = image_cv2.copy()

            global hsv_high, hsv_low

            while True:
                if Mod:
                    dst = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2HSV)  # BGR转HSV
                    dst = cv2.inRange(dst, hsv_low, hsv_high)  # 通过HSV的高低阈值，提取图像部分区域
                    # mask = cv.inRange(dst, lowerb, upperb)
                    black = cv2.medianBlur(dst, 9)
                    contours, hierarchy = cv2.findContours(black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    # print contours
                    goal = []
                    if contours:
                        for h in range(len(contours)):
                            arr = contours[h].tolist()
                            list = []
                            for i in arr:
                                list.append(i[0])

                            max_x = np.amax(list, axis=0)[0]
                            max_y = np.amax(list, axis=0)[1]
                            min_x = np.amin(list, axis=0)[0]
                            min_y = np.amin(list, axis=0)[1]

                            cv2.rectangle(image_1, (min_x, min_y), (max_x, max_y), (0, 0, 255), 1)
                            position = [(min_x, min_y), (max_x, max_y)]
                            goal.append(position)
                        # print goal
                        max = Cont
                        max_i = []
                        max_v = []
                        for i, v in goal:
                            x = v[0] - i[0]
                            y = v[1] - i[1]
                            # print x, y
                            if y - x > max:
                                max = y - x
                                max_i.insert(0, i)
                                max_v.insert(0, v)
                        if max != Cont:
                            # print max
                            cv2.rectangle(image_1, max_i[0], max_v[0], (255, 0, 0), 1)
                            # return [max_i[0], max_v[0]]

                    _, dst_red = Circle_dec(dst, image_2)
                    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
                    dst_red = cv2.cvtColor(dst_red, cv2.COLOR_GRAY2BGR)
                    dst_green = Green(image_cv2,green)  # 取绿色
                    stitch_h = Stitch_imagesh(dst, dst_red)
                    stitch_h_1 = Stitch_imagesh(image_1, dst_green)
                    stitch_w = Stitch_imagesw(stitch_h, stitch_h_1)
                    cv2.imshow('V6.0-by:Fanzhe', stitch_w)

                else:

                    dst_1 = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2HSV)  # BGR转HSV
                    dst_12 = cv2.inRange(dst_1, hsv_low, hsv_high)  # 通过HSV的高低阈值，提取图像红色部分区域
                    dst_1 = cv2.cvtColor(dst_12, cv2.COLOR_GRAY2BGR)

                    dst_green = Green(image_cv2,green)
                    dst_green = cv2.cvtColor(dst_green, cv2.COLOR_BGR2HSV)  # BGR转HSV
                    dst = cv2.inRange(dst_green, hsv_low, hsv_high)  # 通过HSV的高低阈值，提取图像部分区域
                    # print hsv_low,hsv_high
                    image_red, dst_red = Circle_dec(dst, image_1)  # 在绿色背景下取红色

                    _, dst_red_1 = Circle_dec(dst_12, image_2)  # 再单纯取红色背景
                    dst_red_1 = cv2.cvtColor(dst_red_1, cv2.COLOR_GRAY2BGR)  # 将GRAY变成BGR
                    dst_green = Green(image_cv2,green)

                    # print dst.size, image_red.size, dst_red.size, dst_green.size
                    # cv2.imshow('dst', dst)
                    # cv2.imshow('dst_redball', dst_red)
                    # cv2.imshow('redball', image_red)
                    stitch_h = Stitch_imagesh(dst_1,dst_red_1)
                    stitch_h_1 = Stitch_imagesh(image_red, dst_green)
                    stitch_w = Stitch_imagesw(stitch_h, stitch_h_1)
                    cv2.imshow('V6.0-by:Fanzhe', stitch_w)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    hsv_low_temp = hsv_low
                    hsv_high_tempt = hsv_high
                    print ('Low:{}\n High:{}'.format(hsv_low_temp, hsv_high_tempt)
                    print('Adjust:{},{},{},{},{},{}\n'.format(hsv_low_temp[0], hsv_high_tempt[0],
                                                            hsv_low_temp[1], hsv_high_tempt[1],
                                                            hsv_low_temp[2], hsv_high_tempt[2])

                    cv2.destroyWindow('V6.0-by:Fanzhe')
                    break
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    hsv_low_temp = hsv_low
                    hsv_high_tempt = hsv_high
                    print ('Low:{}\n High:{}'.format(hsv_low_temp, hsv_high_tempt)
                    print ('Adjust:{},{},{},{},{},{}\n'.format(hsv_low_temp[0], hsv_high_tempt[0],
                                                            hsv_low_temp[1], hsv_high_tempt[1],
                                                            hsv_low_temp[2], hsv_high_tempt[2])

                    cv2.destroyWindow('V6.0-by:Fanzhe')
                    if Mod==0:
                        Mod=1
                        break
                    elif Mod==1:
                        Mod=0
                        break
    except KeyboardInterrupt:
        exit()
    finally:
        Relax_Camare(imgClient)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.113",
                        help="Robot ip address")
    parser.add_argument("--stand", type=str, default=False,
                        help="Stand robot or not")
    parser.add_argument("--Cam", type=int, default=0,
                        help="Change robot's Camera")
    parser.add_argument("--contour", type=int, default=65,
                        help="Change contours number")
    parser.add_argument("--green", type=str, default='36.47.22.93.255.255',
                        help="Change contours number")

    args = parser.parse_args()
    print('ip :{} \n stand:{} \n Camera:{} \n contour :{}\n '
          'green:{}\n type-g :{}'.format(args.ip,args.stand,args.Cam,args.contour,args.green,type(args.stand)))

    if str(args.stand)=='True':
        Stand_up(args.ip)

    Connect(green=analyse(args.green),Ip=args.ip, CameraId=args.Cam, Cont=args.contour)
