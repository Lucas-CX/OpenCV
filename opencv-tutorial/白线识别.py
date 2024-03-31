class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motionProxy = ALProxy("ALMotion")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.camProxy = ALProxy("ALVideoDevice")
    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        import cv2
        import numpy as np
        from PIL import Image
        import vision_definitions
        maxstepx = 0.04
        maxstepy = 0.14
        maxsteptheta = 0.4
        maxstepfrequency = 0.5
        stepheight = 0.02
        torsowx = 0.0
        torsowy = 0.0
        moveConfig = [["MaxStepX", maxstepx],
                       ["MaxStepY", maxstepy],
                       ["MaxStepTheta", maxsteptheta],
                       ["MaxStepFrequency", maxstepfrequency],
                       ["StepHeight", stepheight],
                       ["TorsoWx", torsowx],
                       ["TorsoWy", torsowy]]
        def selsct(a):
            b = []
            a.sort(key=lambda x: x[0])
            b.append(a[0])
            for i in range(1, len(a)):
                if a[i][0] - a[i-1][0] >= 0.05: #相当于什么误差？
                    b.append(a[i])
            print b
            return b
        def houghlines(frame):
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            lowera = np.array([0, 0, 221])   #np是numpy模块
            uppera = np.array([180, 30, 255])
            mask1 = cv2.inRange(hsv, lowera, uppera)
#            cv2.imshow("2", mask1)
            kernel = np.ones((3, 3), np.uint8)  #什么意思
            mask = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)  #需要研究
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   #需要研究
            newline = cv2.HoughLines(mask, 1, np.pi / 180, 200)   #霍夫直线
            print type(newline)
            if str(type(newline)) == "<type 'numpy.ndarray'>":  #尖括号是什么鬼？
                new = np.ndarray.tolist(newline)
                print new
            else:
                new = [None]
            return new[0]
        def getimage():
            self.camProxy.openCamera(1)
            self.camProxy.setActiveCamera(1)
            resolution = vision_definitions.kQVGA  #分配器？
            colorSpace = vision_definitions.kBGRColorSpace #vision_definitions这些哪里来的？
            fps = 30
            nameId = self.camProxy.subscribeCamera("python_GVM", 1, resolution, colorSpace, fps)
            self.camProxy.setCamerasParameter(nameId, 22, 2)
            naoImage = self.camProxy.getImageRemote(nameId)
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            array = naoImage[6]
            im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
            self.camProxy.releaseImage(nameId)
            self.camProxy.unsubscribe(nameId)
            return np.array(im)  #实例化哪里来的？返回得到了什么？
        def drawline(a): #获得数据的物理意义是什么
            for rho, theta in a:
                if theta < 1.5 and theta > 0.7:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    # print "a,b:-------------"
                    # print a, b
                    x0 = a * rho
                    y0 = b * rho
                    # print "x0,y0:"
                    # print x0, y0
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))
                    # print x1, y1
                    # print x2, y2
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    return rho, theta
                elif theta > 1.57 and theta < 2.2:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    # print "a,b:-------------"
                    # print a, b
                    x0 = a * rho
                    y0 = b * rho
                    # print "x0,y0:"
                    # print x0, y0
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))
                    # print x1, y1
                    # print x2, y2
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    return abs(rho), theta
            return 100, 1.5
        self.motionProxy.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
        self.motionProxy.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
        try:
            frame = getimage()
            newline = houghlines(frame)
            self.log("newline=%s" %newline)
            newline1 = selsct(newline)
            rho, theta = drawline(newline1) #是什么操作？应该传入两个
            self.log((rho,theta))
            print rho, theta


            if 1.63-theta > 0.0:  #如果小于1.63 角度是哪里的夹角？
                self.motionProxy.setMoveArmsEnabled(False, False)
                self.motionProxy.moveTo(0, 0, 1.68 - theta, moveConfig) #值哪里来？
                self.log("小于1.63，执行一次")
                self.log("1.63-theta:%s"%(1.68-theta))
            else:
                for i in range(2):
                    frame = getimage()
                    newline = houghlines(frame)
                    self.log("newline=%s"%newline)
                    newline1 = selsct(newline)
                    rho, theta = drawline(newline1)
                    self.log((rho,theta))
                    print rho, theta
                    self.motionProxy.setMoveArmsEnabled(False, False)
                    self.motionProxy.moveTo(0, 0, 1.63 - theta, moveConfig)  #值哪里来？
                    self.log("小于1.63，执行一次")
                    self.log("大于1.63，执行一次")
                    self.log("1.63-theta:%s"%(1.63-theta))
            self.onStopped()
        except:
            self.log("no line")
            self.onStopped()

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
#        self.onStopped() #activate the output of the box