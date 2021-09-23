import numpy as np


class PurePursuitControl:
    def __init__(self, kp=1, Lfc=10):
        self.path = None
        self.kp = kp
        self.Lfc = Lfc

    def set_path(self, path):
        self.path = path.copy()

    def _search_nearest(self, pos):
        min_dist = 99999999
        min_id = -1
        for i in range(self.path.shape[0]):
            dist = (pos[0] - self.path[i, 0])**2 + \
                (pos[1] - self.path[i, 1])**2
            if dist < min_dist:
                min_dist = dist
                min_id = i
        return min_id, min_dist

    # State: [x, y, yaw, v, l]
    def feedback(self, state):
        # Check Path
        if self.path is None:
            print("No path !!")
            return None, None

        # Extract State
        x, y, yaw, v, l = state["x"], state["y"], state["yaw"], state["v"], state["l"]

        # Search Front Target
        min_idx, min_dist = self._search_nearest((x, y))

        # todo
        #####################################################################

        # all parameter name (ex:alpha) comes from the Slides
        # You need to finish the pure pursuit control algo

        # step by step
        # first, you need to calculate the look ahead distance Ld by formula
        #
        # second, you need to find a point(target) on the path which distance
        # between the path and model is as same as the Ld
        #
        # hint: (you first need to find the nearest point and then find the
        # point(target) backward, this will make your model won't go back)

        # hint: (if you can not find a point(target) on the path which distance
        #  between the path and model is as same as the Ld, you need to
        # find a similar one)

        # third, you need to calculate alpha
        # now, you can calculate the delta

        # The next_delta is Pure Pursuit Control's output
        # The target is the point on the path which you find
        #####################################################################

        # calculate nearest distance Ld
        Ld = self.kp * v + self.Lfc

        # search the following point as same as Ld
        distance = min_dist
        idx = min_idx

        while distance < Ld and (idx+1) < len(self.path[:, 0]):
            idx += 1
            # find distance between next idx and car
            distance = (x-self.path[idx, 0])**2 + (y-self.path[idx, 1])**2
        
        # update alpha
        alpha = np.arctan2(self.path[idx, 1]-y, self.path[idx, 0]-x) - np.deg2rad(yaw)

        # update delta
        next_delta = np.rad2deg(np.arctan2(2*l*np.sin(alpha), distance))

        target = self.path[idx]

        return next_delta, target


if __name__ == "__main__":
    import cv2
    import path_generator
    import sys
    sys.path.append("../")
    from bicycle_model import KinematicModel

    # Path
    path = path_generator.path2()
    img_path = np.ones((600, 600, 3))
    for i in range(path.shape[0]-1):
        cv2.line(img_path, (int(path[i, 0]), int(path[i, 1])), (int(
            path[i+1, 0]), int(path[i+1, 1])), (1.0, 0.5, 0.5), 1)

    # Initialize Car
    car = KinematicModel()
    start = (50, 300, 0)
    car.init_state(start)
    controller = PurePursuitControl(kp=1, Lfc=10)
    controller.set_path(path)

    while(True):
        print("\rState: "+car.state_str(), end="\t")
        # ================= Control Algorithm =================
        # PID Longitude Control
        end_dist = np.hypot(path[-1, 0]-car.x, path[-1, 1]-car.y)
        target_v = 40 if end_dist > 265 else 0
        next_a = 0.1*(target_v - car.v)

        # Pure Pursuit Lateral Control
        state = {"x": car.x, "y": car.y,
                 "yaw": car.yaw, "v": car.v, "l": car.l}
        next_delta, target = controller.feedback(state)
        car.control(next_a, next_delta)
        # =====================================================

        # Update & Render
        car.update()
        img = img_path.copy()
        cv2.circle(img, (int(target[0]), int(target[1])),
                   3, (1, 0.3, 0.7), 2)  # target points
        img = car.render(img)
        img = cv2.flip(img, 0)
        cv2.imshow("Pure-Pursuit Control Test", img)
        k = cv2.waitKey(1)
        if k == ord('r'):
            car.init_state(start)
        if k == 27:
            print()
            break
