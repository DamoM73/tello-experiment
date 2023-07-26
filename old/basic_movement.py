from djitellopy import tello
from time import sleep

# prepare the drone
drone = tello.Tello()
drone.connect()

# take off proceedure
flight_time_start = drone.get_flight_time()
sleep(1.0)
drone.takeoff()

# ---- put your flight commands under this comment ---- #

drone.move_forward(50)
drone.move_left(50)
drone.move_back(50)
drone.move_right(50)
drone.rotate_clockwise(180)
drone.rotate_counter_clockwise(180)

# landing proceedure
drone.land()
flight_time_end = drone.get_flight_time()
print(f"\nFlight time: {flight_time_end - flight_time_start}sec")
print(f"Battery remaining: {drone.get_battery()}%")