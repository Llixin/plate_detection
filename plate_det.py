import cv2
import numpy as np

"""霍夫圆检测，放弃：圆柱是固定的，不需要检测
def circles_det(img):
    h = img.shape[0]
    w = img.shape[1]
    if h * w > 6000:
        dp = 1
    else:
        dp = 2  # 分辨率不足时，提高dp参数阈值
    d = (int)(w / 2)  # d表示检测到的圆心之间的最小距离
    r_min = (int)((w / 4.2) / 2)  # 最小半径
    r_max = (int)((w / 3.2) / 2)  # 最大半径

    # 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 形态学腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=3)

    gray = cv2.medianBlur(gray, 5)
    # ret, th1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
    # th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 5)

    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(th2, kernel, iterations=1)
    # dilation = cv2.dilate(erosion, kernel, iterations=1)

    # 边缘检测
    imgray = cv2.Canny(erosion, 30, 100)

    # 霍夫圆检测
    circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, dp, d, param1=100, param2=5, minRadius=r_min,
                               maxRadius=r_max)
    try:
        circles = np.uint16(np.around(circles))
    except TypeError:
        print("未检测到圆！")
        return -1

    # 画圆
    count = 0
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 1)
        # draw the center of the circle
        cv2.circle(img, (i[0], i[1]), 1, (0, 0, 255), 1)
        count = count + 1
        if count >= 2:
            break

    return circles[0]
"""


def plate_det(img):
    # 灰度化
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except Exception:
        print("图片错误")
        exit()

    # 获取尺寸
    h = img.shape[0]
    w = img.shape[1]
    # 检测区域范围
    top = int(h * 2 / 5)
    bottom = int(h / 2)
    left = int(w / 2)
    right = int(w)
    cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 1)

    # 边缘检测
    try:
        edges = cv2.Canny(gray, 50, 200)
    except Exception:
        print("边缘检测出错")
        exit()

    minLineLength = w / 10  # 最小线段长度
    if h * w > 6000:
        maxLineGap = 5  # 线段允许间隔的最大距离，超过此距离则判定为两条线段
    else:
        maxLineGap = 1
    # 直线检测
    try:
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, minLineLength, maxLineGap)
    except Exception:
        print("直线检测出错")
        exit()

    # 遍历检测到的每条线段，若在指定范围内存在线段，则返回1
    count = 0
    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            cv2.line(img, (x1, y1), (x2, y2), (i * 20, 100 + i * 20, 255), 1)
            if left < x1 < right and top < y1 < bottom or left < x2 < right and top < y2 < bottom:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
                count = count + 1
    # print("count:", count)
    if count > 1:
        return 1
    return 0
