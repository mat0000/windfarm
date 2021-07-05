#!/usr/bin/python

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import psycopg2
from config import config
import time
import datetime
import math
import statistics
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# connection
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan_direction = AnalogIn(mcp, MCP.P3)
chan_speed = AnalogIn(mcp, MCP.P2)

# setup 
interval_gust = 2.5 # gust measurement interval (in seconds)
interval_wind = 10 # wind measurement interval (in seconds)

# map volt: angle 
volts = {2.5: 0, 1.5: 45, 0.3: 90, 0.6: 135, 0.9: 180, 2.0: 225, 3.0: 270, 2.9: 315}

# map angle: direction
directions = {0: "NE", 45: "E", 90: "SE", 135: "S", 180: "SW", 225: "W", 270: "NW", 315: "N"}

# function to get average angle (in degrees)
def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

# function to make binary readout
# (digital inputs are 128, 65472 and occasionally some intermediates)
def spin(value):
    if(value == 65472):
        return 1
    else:
        return 0

# function to convert frequency to kmh
def convert_to_kmh(frequency):
    # m/s = Hz * 0.34 (from sensor documentation)
    # kmh = m/s * 3.6
    kmh = frequency * 0.34 * 3.6
    return(kmh)

# function to get wind speed (in kmh) and angle (degrees)
# short term readout (using interval_gust timw window)
def get_speed_dir():
    wind_count = 0 # spin counter
    spin_prev = 0 # signal change 
    directions = [] # vector of temporary wind directions
    t_end = time.time() + interval_gust # time window
    while time.time() < t_end:
        
        # detect signal change
        if(spin_prev != spin(chan_speed.value)): # two changes for 1 pulse!
            wind_count = wind_count + 1
            spin_prev = spin(chan_speed.value)
        
        # detect wind direction
        d_direction = round(chan_direction.voltage, 1)
        if d_direction in volts:
            directions.append(volts[d_direction])

    # NEED ADDITIONAL CALIBRATION (use fixed number of rotations)
    spin_frequency = wind_count / interval_gust / 2
    speed = round(convert_to_kmh(spin_frequency), 1)
    direction = get_average(directions)
    return([speed, direction])

# function to get wind and gust speed (in kmh) and wind direction (degrees)
def get_speed_gusts_dir():
    gust_speeds = []
    gust_directions = []
    t_end = time.time() + interval_wind # define time window
    while time.time() < t_end:
        data = get_speed_dir()
        gust_speeds.append(data[0])
        gust_directions.append(data[1])
    
    # wind as average of gusts
    wind_speed = round(statistics.mean(gust_speeds), 1)

    # gusts as max gust speed
    gust_speed = max(gust_speeds)

    # wind direction as average angle over long time period
    wind_direction = round(get_average(gust_directions))

    # return vector: average wind speed, gust speed (kmh) and direction (angle)
    return([wind_speed, gust_speed, wind_direction])

print('Collecting data using ' + str(interval_wind) + 's time window...')
data = get_speed_gusts_dir()
wind_speed = data[0]
gust_speed = data[1]
wind_direction = data[2]
time_cur = datetime.datetime.now().time()
time_cur = time_cur - datetime.timedelta(microseconds=time_cur.microsecond)

print(str(time_cur))
print('Wind speed: ' + str(wind_speed) + ' kmh.')
print('Gust speed: ' + str(gust_speed) + ' kmh.')

if wind_direction in directions:
    print('Wind direction: ' + str(wind_direction) + ' degrees (' + directions[wind_direction] + ')')
else:
    print('Wind direction: ' + str(wind_direction) + ' degrees.')
