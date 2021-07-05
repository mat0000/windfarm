# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
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
volts = [2.5, 1.5, 0.3, 0.6, 0.9, 2.0, 3.0, 2.9]
while True:
    direction = round(chan.voltage, 1)
    if not direction in volts:
        print('Unknown value: ' + str(direction))
    else:
        print('Match: ' + str(direction))
