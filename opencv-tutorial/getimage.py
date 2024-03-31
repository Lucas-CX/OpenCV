# -*- encoding: UTF-8 -*-
# 黄杆识别

import cv2
import time
import math
import almath
import cv2.cv as cv
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
        self.red_hsv_low = np.array([0, 116, 0])
        self.red_hsv_high = np.array([36, 255, 255])
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
        print self.name_id
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
        self.name_id = self.camera.subscribeCamera('pyt111hon1121', camera_id, self.resolution, self.color_space, self.fps)
        nao_image = self.camera.getImageRemote(self.name_id)
        for i in range(0, 100, 1):
            cv2.imwrite("C:/Users/lcx/Desktop/image"+str(i)+".png",image)
            time.sleep(2)
        self.camera.releaseImage(self.name_id)
        self.camera.unsubscribe(self.name_id)

        image_wight, image_height = nao_image[0], nao_image[1]
        image_array = nao_image[6]
        # image = Image.fromstring('RGB', (image_wight, image_height), image_array)
        image = Image.frombytes('RGB', (image_wight, image_height), image_array)  # 注意测试用frombytes,机器人上用fromstring
        image = np.array(image)

        return image


if __name__=='__main__':
    reco = Recognize('192.198.0.104')
    img = reco.getimage(0)

