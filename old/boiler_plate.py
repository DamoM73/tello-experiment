from djitellopy import tello
from time import sleep

# prepare the drone
drone = tello.Tello()
drone.connect()

# takeoff proceedure
sleep(1.0)
flight_time_start = drone.get_flight_time()
drone.takeoff()

# ---- put your flight commands under this comment ---- #


while True:
    img = drone.get_frame_read().frame
    

# landing proceedure
drone.land()
flight_time_end = drone.get_flight_time()
print(f"\nFlight time: {flight_time_end - flight_time_start}sec")
print(f"Battery remaining: {drone.get_battery()}%")
drone.end()