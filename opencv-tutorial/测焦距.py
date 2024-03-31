# -*- encoding: UTF-8 -*-
# 测距用

import cv2
import numpy as np
from PIL import Image
from naoqi import ALProxy
import vision_definitions


class Recognize:
    def __init__(self, ip):
        self.camera = ALProxy('ALVideoDevice', ip, 9559)
        self.motion = ALProxy('ALMotion', ip, 9559)
        self.memory = ALProxy("ALMemory", ip, 9559)
        self.redballdetection = ALProxy("ALRedBallDetection", ip, 9559)
        self.landmark = ALProxy("ALLandMarkDetection", ip, 9559)
        self.tts = ALProxy("ALTextToSpeech", ip, 9559)

        self.red_hsv_low_1 = np.array([0, 43, 46])
        self.red_hsv_high_1 = np.array([10, 255, 255])
        self.red_hsv_low_2  = np.array([156, 43, 46])  # 初始化
        self.red_hsv_high_2 = np.array([180, 255, 255])

        self.green_hsv_low = np.array([52, 44, 28])
        self.green_hsv_high = np.array([90, 255, 255])
        self.yellow_hsv_low = np.array([0, 86, 0])
        self.yellow_hsv_high = np.array([44, 255, 255])
        self.write_hsv_low = np.array([0, 0, 221])
        self.write_hsv_high = np.array([180, 30, 255])
        self.yellow_poll_argu = 40
        self.resolution = vision_definitions.kQVGA
        self.color_space = vision_definitions.kBGRColorSpace
        self.fps = 30
        self.name_id = None
        self.redballdetection.subscribe("redBallDetected")  # 打开红球识别

    def __del__(self):
        if self.name_id is not None:
            self.camera.releaseImage(self.name_id)
            self.camera.unsubscribe(self.name_id)
            # self.redballdetection.unsbuscribe("redBallDetected")

    def getimage(self, camera_id=1):
        """
        获取机器人内部图像，取图像后释放资源
        :param camera_id: 摄像头id，默认下摄像头
        :return: PIL格式的图像（array）
        """
        self.camera.openCamera(camera_id)
        self.camera.setActiveCamera(camera_id)
        self.name_id = self.camera.subscribeCamera('po1', camera_id, self.resolution, self.color_space, self.fps)
        nao_image = self.camera.getImageRemote(self.name_id)
        self.camera.releaseImage(self.name_id)
        self.camera.unsubscribe(self.name_id)

        image_wight, image_height = nao_image[0], nao_image[1]
        image_array = nao_image[6]
        # image = Image.fromstring('RGB', (image_wight, image_height), image_array)
        image = Image.frombytes('RGB', (image_wight, image_height), image_array)  # 注意测试用frombytes,机器人上用fromstring
        image = np.array(image)

        return image


    def debug(self, camera_id=0):
        '''
        黄杆识别v1.0
        思路： 排除非长方形的内容 1.0*w/h =0.25为阈值一，w<35为阈值二
        其他思路：将图像的所有矩阵画在原图上，再进行检测 ，使用分水岭算法，水滴算法解决异常连接问题
        :return:
        '''
        image = self.getimage(camera_id)
        cv2.imshow('origin', image)
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image_flt = cv2.inRange(image_hsv, self.write_hsv_low, self.write_hsv_high)
        cv2.imshow('image_flt', image_flt)
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(image_flt, cv2.MORPH_OPEN, kernel)
        cv2.imshow('opening', opening)
        # imageG = cv2.GaussianBlur(opening, (9, 9), 0)
        # cv2.imshow('imageG', imageG)
        contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0:
            return None
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(image, (160, 0), (160+1, 120), (255, 0, 0), 2)
            cv2.putText(image, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            print '标号:{},宽:{},高:{}'.format(i, w, h)
        cv2.imshow('contours', image)


if __name__=='__main__':
    reco = Recognize('192.168.0.104')
    reco.debug()
    if cv2.waitKey(0) & 0xFF == ord('q'):
        pass
