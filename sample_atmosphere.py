from djitellopy import tello


def fahrenheit_to_celsius(temp_f: float):
    return round((temp_f - 32.0) / 1.8,1)

drone = tello.Tello()
drone.connect()

readings = []

drone.takeoff()

for _ in range(5):
    readings.append((drone.get_height(), fahrenheit_to_celsius(drone.get_temperature()), drone.get_barometer()))
    drone.move_up(30)

drone.land()

print(drone.get_battery())

for reading in readings:
    print(f"At {reading[0]}cm - temp: {reading[1]}C air pressure: {reading[2]}atm")

