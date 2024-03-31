import argparse
import time
import cv2
import numpy as np

# 配置参数
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
                help="OpenCV object tracker type")
args = vars(ap.parse_args())

# opencv已经实现了的追踪算法
OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,  # 比KCF稍精确，但速度不如后者。（如果追求高准确度，又能忍受慢一些的速度，那么就用CSRT
    "kcf": cv2.TrackerKCF_create,	# 比上一个追踪器更精确，但是失败率比较高,如果对准确度的要求不苛刻，想追求速度，那么就选KCF
    "boosting": cv2.TrackerBoosting_create, # 和Haar cascades（AdaBoost）背后所用的机器学习算法相同，但是距其诞生已有十多年了。这一追踪器速度较慢，并且表现不好，但是作为元老还是有必要提及的
    "mil": cv2.TrackerMIL_create,  # 比上一个追踪器更精确，但是失败率比较高
    "tld": cv2.TrackerTLD_create, # TLD的误报非常多，所以不推荐
    "medianflow": cv2.TrackerMedianFlow_create, # 在报错方面表现得很好，但是对于快速跳动或快速移动的物体，模型会失效。
    "mosse": cv2.TrackerMOSSE_create  # 纯粹想节省时间就用MOSSE
}

# 实例化OpenCV's multi-object tracker
trackers = cv2.MultiTracker_create()
vs = cv2.VideoCapture(args["video"])

# 视频流
while True:
    # 取当前帧
    frame = vs.read()
    # (true, data)
    frame = frame[1]
    # 到头了就结束
    if frame is None:
        break

    # resize每一帧
    (h, w) = frame.shape[:2]
    width = 600
    r = width / float(w)
    dim = (width, int(h * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    # 追踪结果
    (success, boxes) = trackers.update(frame)

    # 绘制区域
    for box in boxes:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 显示
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10) & 0xFF

    if key == ord("s"):
        # 选择一个区域，按
        box = cv2.selectROI("Frame", frame, fromCenter=False,
                            showCrosshair=True)

        # 创建一个新的追踪器
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
        trackers.add(tracker, frame, box)

    # 退出
    elif key == 27:
        break
vs.release()
cv2.destroyAllWindows()
