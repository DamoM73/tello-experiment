from djitellopy import tello
from time import sleep
import cv2

# prepare the drone
drone = tello.Tello()
drone.connect()

# takeoff proceedure
flight_time_start = drone.get_flight_time()
sleep(1.0)
flying = True
drone.takeoff()


# ---- put your flight commands under this comment ---- #
drone.streamon()

while flying:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360,240))
    cv2.imshow("Image",img)
    cv2.waitKey(1)

# landing proceedure
drone.land()
flight_time_end = drone.get_flight_time()
print(f"\nFlight time: {flight_time_end - flight_time_start}sec")
print(f"Battery remaining: {drone.get_battery()}%")