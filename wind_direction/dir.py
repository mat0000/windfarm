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

# setup 
interval_gust = 2.5 # gust measurement interval (in seconds)

# map volt: angle 
volts = {
    2.5: 0,
    1.5: 45,
    0.3: 90,
    0.6: 135,
    0.9: 180,
    2.0: 225,
    3.0: 270,
    2.9: 315
    }

# function to get average angle (in degrees)
def get_average(angles):
    
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    if(flen != 0):
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
    else:
        return 'NULL'

def get_direction():
    t_end = time.time() + interval_gust # time window
    directions = []
    while time.time() < t_end:
        d_direction = round(chan_direction.voltage, 1)
        if d_direction in volts:
            directions.append(volts[d_direction])
    direction = get_average(directions)
    return(direction)

while True:
    print('Wind direction: ' + str(get_direction()) + " (degrees)")
    time.sleep(1)