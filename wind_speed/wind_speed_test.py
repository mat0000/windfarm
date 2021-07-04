# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import statistics
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P2)


interval_gust = 5 # gust measurement interval (in seconds)
interval_wind = 60

# make binary readout
def spin(value):
    if(value == 65472):
        return 1
    else:
        return 0

def spin_frequency(interval_gust):

    wind_count = 0 # spin counter
    spin_prev = 0 # signal change 
    t_end = time.time() + interval_gust
    while time.time() < t_end:
        
        # detect signal change
        if(spin_prev != spin(chan.value)):
            wind_count = wind_count + 1
            # print("spin: " + str(wind_count))
            spin_prev = spin(chan.value)

    # NEED ADDITIONAL CALIBRATION (use fixed number of rotations)
    return(wind_count / interval)

def convert_to_kmh(frequency):
    kmh = frequency * 0.34 * 3.6
    return(kmh)

def get_wind_speed(interval_wind, interval_gust):
    store_speeds = []
    t_end = time.time() + interval_wind
    while time.time() < t_end:
        gust_speeds.append.convert_to_kmh(spin_frequency(interval_gust))
    
    wind_average = statistics.mean(store_speeds)
    wind_gust = max(store_speeds)
    return([wind_average, wind_gust])

wind_speed = get_wind_speed(interval_wind, interval_gust)
print("wind speed: " + str(wind_speed[0]) + "km/h")
print("wind gust: " + str(wind_speed[1]) + "km/h")