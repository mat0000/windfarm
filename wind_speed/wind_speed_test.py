# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from gpiozero import Button

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P2)

wind_count = 0
spin_prev = 0

def spin(value):
    if(value == 65472):
        return 1
    else:
        return 0

while True:
    if(spin_prev != spin(chan.value)):
        wind_count = wind_count + 1
        print("spin: " + str(wind_count))
        print("val: " + str(chan.value))
        spin_prev = spin(chan.value)
    else:
        print("val: " + str(chan.value))
    time.sleep(0.01)

