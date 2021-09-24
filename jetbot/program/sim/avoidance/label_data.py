import glob
import cv2
import os
import numpy as np
from uuid import uuid1

images = [cv2.imread(file) for file in glob.glob("dataset_raw/*.jpg")]

DATASET_DIR = 'dataset_xy'


def xy_uuid(x, y):
    return 'xy_%03d_%03d_%s' % (x * 50 + 50, y * 50 + 50, uuid1())


try:
    os.makedirs(DATASET_DIR)
except FileExistsError:
    print('Directories not created becasue they already exist')


def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 15, (255, 0, 0), -1)
        mouseX, mouseY = x, y


for image in images:
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_circle)
    img = image.copy()
    while(1):
        cv2.imshow('image', img)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('a'):
            uid = xy_uuid(mouseX, mouseY)
            image_path = os.path.join(DATASET_DIR, uid + '.jpg')
            cv2.imwrite(image_path, image)
            break
        elif k == ord('b'):
            break
