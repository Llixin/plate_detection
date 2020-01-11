import sys
import cv2
import numpy as np

img = cv2.imread(sys.argv[1])
#img = cv2.imread("D:\pannel\knob_det\plate_det\img\plate.png")

w = img.shape[1]
if w > 100:
    dp = 1
else:
    dp = 2
d = (int)(w / 2)
r_min = (int)((w / 4.2) / 2)
r_max = (int)((w / 3.2) / 2)
print(r_min, r_max, d)

GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 形态学腐蚀
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
GrayImage = cv2.morphologyEx(GrayImage, cv2.MORPH_OPEN, kernel, iterations=3)
# cv2.imwrite('img/open.png', GrayImage)

GrayImage = cv2.medianBlur(GrayImage, 5)
ret, th1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(GrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
th3 = cv2.adaptiveThreshold(GrayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 5)

kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(th2, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=1)

imgray = cv2.Canny(erosion, 30, 100)

circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, dp, d, param1=100, param2=5, minRadius=r_min, maxRadius=r_max)
circles = np.uint16(np.around(circles))
print(circles[0])

count = 0
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 1)
    # draw the center of the circle
    cv2.circle(img, (i[0], i[1]), 1, (0, 0, 255), 1)

    count = count + 1
    if count == 2:
        break
print(len(circles[0, :]))

cv2.imshow('detected circles', img)
# cv2.imwrite('img/plate_result.png', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
