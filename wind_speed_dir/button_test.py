from gpiozero import Button
import time

chan_speed = Button(17)
wind_count = 0
interval_gust = 4

def spin():
    global wind_count
    wind_count = wind_count + 1
    print("spin" + str(wind_count))
    return(spin)

def convert_to_kmh(frequency):
    # m/s = Hz * 0.34 (from sensor documentation)
    # kmh = m/s * 3.6
    kmh = frequency * 0.34 * 3.6
    return(kmh)

def get_speed():
    global wind_count
    wind_count = 0 # spin counter
    t_end = time.time() + interval_gust # time window
    while time.time() < t_end:
        chan_speed.when_pressed = spin
        time.sleep(0.1)

    # NEED ADDITIONAL CALIBRATION (use fixed number of rotations)
    spin_frequency = wind_count / interval_gust
    speed = round(convert_to_kmh(spin_frequency), 1)
    time.sleep(0.1)
    return(speed)

while True:
    print(str(get_speed()) + "Hz")