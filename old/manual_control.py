from djitellopy import tello
import cv2, math, time

# prepare the drone
drone = tello.Tello()
drone.connect()
drone.streamon()
frame_read = drone.get_frame_read()

# takeoff proceedure
time.sleep(1.0)
flight_time_start = drone.get_flight_time()
drone.takeoff()

# ---- put your flight commands under this comment ---- #


while True:
    img = frame_read.frame
    cv2.imshow("Drone", img)
    
    key = cv2.waitKey(1) & 0xff
    
    if key == 27:
        break
    elif key == ord("w"):
        drone.move_forward(30)
    elif key == ord("k"):
        drone.move_back(30)
    elif key == ord("a"):
        drone.move_left(30)
    elif key == ord("d"):
        drone.move_right(30)
    elif key == ord("e"):
        drone.rotate_clockwise(30)
    elif key == ord("q"):
        drone.rotate_counter_clockwise(30)
    elif key == ord("r"):
        drone.move_up(30)
    elif key == ord("f"):
        drone.move_down(30)

# landing proceedure
drone.land()
flight_time_end = drone.get_flight_time()
print(f"\nFlight time: {flight_time_end - flight_time_start}sec")
print(f"Battery remaining: {drone.get_battery()}%")
drone.end()