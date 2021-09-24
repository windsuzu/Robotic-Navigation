from jetbotSim import Robot, Camera
import numpy as np
import cv2
import torch.nn.functional as F
import torchvision
import torch

blocked_left = 0
blocked_right = 0

model = torchvision.models.alexnet(pretrained=False)
model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, 3)
model.load_state_dict(torch.load('best_avoidance_model.pth'))

device = torch.device('cuda')
model = model.to(device)

mean = 255.0 * np.array([0.485, 0.456, 0.406])
stdev = 255.0 * np.array([0.229, 0.224, 0.225])

normalize = torchvision.transforms.Normalize(mean, stdev)

def preprocess(camera_value):
    global device, normalize
    x = camera_value
    x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    x = x.transpose((2, 0, 1))
    x = torch.from_numpy(x).float()
    x = normalize(x)
    x = x.to(device)
    x = x[None, ...]
    return x


def execute(change):
    global robot, blocked_left, blocked_right

    img = cv2.resize(change["new"], (640, 360))
    x = preprocess(img)
    y = model(x)
    y = F.softmax(y, dim=1)

    # 0: block is on the left
    # 1: block is on the right
    # 2: free
    i = torch.argmax(y.flatten())
    prob = y.flatten()[i]

    # Visualize
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([37, 148, 58])
    upper_red = np.array([255, 255, 236])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(img, img, mask=mask)

    coord = cv2.findNonZero(mask)
    left = np.min(coord, axis=0)
    right = np.max(coord, axis=0)
    try:
        line_mean = int(np.mean([left[0][0], right[0][0]]))
        dist = 320 - line_mean
        if blocked_left > 0:
            if blocked_left > 24:
                robot.backward(0.15)
            elif blocked_left > 12:
                robot.set_motor(0.25, 0.18)
            else:
                robot.set_motor(0.18, 0.25)
            blocked_left -= 1

        elif blocked_right > 0:
            if blocked_right > 24:
                robot.backward(0.15)
            elif blocked_right > 12:
                robot.set_motor(0.18, 0.25)
            else:
                robot.set_motor(0.25, 0.18)
            blocked_right -= 1

        elif i != 2 and prob > 0.75:
            if i == 0:
                print("block left detected")
                blocked_left += 30
            elif i == 1:
                print("block right detected")
                blocked_right += 30

        else:
            if dist >= -20 and dist <= 20:
                robot.forward(0.2)
            elif dist > 20:
                robot.left(0.002 * dist)
            else:
                robot.right(0.002 * -dist)

    except:
        robot.stop()

    cv2.imshow("camera", img)
    cv2.imshow('res', res)


robot = Robot()
camera = Camera()
camera.observe(execute)
