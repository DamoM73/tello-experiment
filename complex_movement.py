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
drone.go_xyz_speed(100,100,0,60)
# drone.curve_xyz_speed(40,20,0,100,100,0,60)

"""drone.send_rc_control(0,50,0,0)
sleep(1)
drone.send_rc_control(0,0,0,0)
sleep(1)"""

# landing proceedure
drone.send_rc_control(0,0,0,0)
drone.land()
flight_time_end = drone.get_flight_time()
print(f"\nFlight time: {flight_time_end - flight_time_start}sec")
print(f"Battery remaining: {drone.get_battery()}%")
drone.end()