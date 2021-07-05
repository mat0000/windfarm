# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import datetime
import statistics
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P3)

count = 0
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


# t_end = time.time() + 5 # time window
# while time.time() < t_end:

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

def get_direction():
    t_end = time.time() + 3 # time window
    data = []
    while time.time() < t_end:
        voltage = round(chan.voltage, 1)
        if not voltage in volts:
            print('Unknown value: ' + str(voltage))
        else:
            data = data.append(volts[voltage])
            print('Match: ' +  str(voltage) + ' ' + str(volts[voltage]))
    return(statistics.mean(data))

print('direction angle ' + str(get_direction()))