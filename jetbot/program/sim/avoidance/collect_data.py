from jetbotSim import Robot, Camera
import cv2

frames = 0

def execute(change):
    global robot, frames
    # print("\rFrames", frames, end="")
    frames += 1
    print(frames)

    if frames == 1:
        robot.forward(0.2)
    if frames == 120:
        robot.set_motor(0.1, 0.13)
    if frames == 200:
        robot.set_motor(0.14, 0.11)
    if frames == 250:
        robot.set_motor(0.11, 0.1)
    if frames == 650:
        robot.set_motor(0.12, 0.1)
    if frames == 1100:
        robot.set_motor(0.1, 0.11)
    if frames == 1200:
        robot.set_motor(0.12, 0.1)
    if frames == 1450:
        robot.set_motor(0.1, 0.11)
    if frames == 1550:
        robot.set_motor(0.117, 0.1)
    if frames == 1700:
        robot.stop()


    # Visualize
    img = cv2.resize(change["new"], (640, 360))
    if frames % 10 == 0:
        cv2.imwrite('dataset_raw/{}.jpg'.format(frames), img)
    # cv2.imshow("camera", img)


robot = Robot()
camera = Camera()
camera.observe(execute)
  