# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import datetime
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

while True:
    voltage = round(chan.voltage, 1)

    if not voltage in volts:
        print('Unknown value: ' + str(voltage) + ' ' + str(volts[voltage]))
    else:
        print('Match: ' +  str(voltage) + ' ' + str(volts[voltage]))
