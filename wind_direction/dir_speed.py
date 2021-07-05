# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import datetime
import math
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

# function to get short time spin frequency (in Hz) and angle (degrees)
def get_freq_dir():
    wind_count = 0 # spin counter
    spin_prev = 0 # signal change 
    directions = [] # vector of temporary wind directions
    t_end = time.time() + interval_gust # time window (gust)
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
    spin_frequency = wind_count / interval / 2
    direction = get_average(directions)
    return([spin_frequency, direction])

data = get_freq_dir()
print('Spin freq: ' + str(data[0]) + 'Dir: ' + str(data[1]))
