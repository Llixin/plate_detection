import os
import sys
import cv2
import matplotlib.pyplot as plt
from plate_det import plate_det

"""单张图片"""
if len(sys.argv) <= 1:
    print("请输入图片")
    exit()
img_path = sys.argv[1]

try:
    img = cv2.imread(img_path)
except Exception:
    print("图片读取失败")
    exit()

print(plate_det(img))
plt.imshow(img)
plt.show()


"""文件夹批量读取
img_path = "F:\\knob_det\\plate-synthetic\\generated-plate\\train\\"
files = os.listdir(img_path)
jpg = []
txt = []
for i in range(len(files)):
    if i % 2 == 0:
        jpg.append(files[i])
    else:
        txt.append(files[i])

fail_num = 0
for i in range(len(jpg)):
    img = cv2.imread(img_path + jpg[i])
    tabel = open(img_path + txt[i], "r").read()
    """"""
    if plate_det(img) != int(tabel[-2]):
        fail_num = fail_num + 1
        # print(jpg[i])
        # plt.imshow(img)
        # plt.show()
print(fail_num)
"""
"""
result = plate_det(img)
print(jpg[i], " tabel:", tabel[-2], " result:", result)
plt.imshow(img)
plt.show()
"""
