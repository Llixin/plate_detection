import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
w = img.shape[1]

# 直线检测
"""线段检测"""
top = 14
bottom = 20
left = 12
right = 20
# 边缘检测
edges = cv2.Canny(gray, 50, 150)
minLineLength = w / 10
maxLineGap = 1
# 直线检测
lines = cv2.HoughLinesP(edges, 10, np.pi / 180, 10, minLineLength, maxLineGap)
# print('len(lines)', len(lines), type(lines))
# print('lines[0].shape', lines[0].shape)
flag = False
for i in range(len(lines)):
    # print(lines[i])
    for x1, y1, x2, y2 in lines[i]:
        cv2.line(img, (x1, y1), (x2, y2), (i * 20, 100 + i * 20, 255), 1)
        if left < x1 < right and top < y1 < bottom or left < x2 < right and top < y2 < bottom:
            flag = True
if flag:
    print(1)
else:
    print(0)


# MSER
"""MSER
mser = cv2.MSER_create(_min_area=50)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
regions, boxes = mser.detectRegions(gray)
for box in boxes:
    x, y, w, h = box
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
print(len(boxes))
"""

# SIFT
"""SIFT
sift = cv2.xfeatures2d.SIFT_create()
kp, des = sift.detectAndCompute(img, None)
img = cv2.drawKeypoints(img, kp, img, color=(255, 0, 255))
"""

# Harris
"""Harris
gray = np.float32(gray)  # 图像转换为float32
dst = cv2.cornerHarris(gray, 2, 3, 0.04)  # result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)  # 图像膨胀
#  Threshold for an optimal value, it may vary depending on the image.
# print(dst)
# img[dst>0.00000001*dst.max()]=[255,0,255] #可以试试这个参数，角点被标记的多余了一些
img[dst > 0.01 * dst.max()] = [255, 0, 255]  # 角点位置用红色标记
# 这里的打分值以大于0.01×dst中最大值为边界
"""

plt.imshow(img)
plt.show()
plt.close()

# cv2.waitKey(0)
# cv2.destroyAllWindows()
