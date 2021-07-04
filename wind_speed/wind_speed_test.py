# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import datetime
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

# while True:
#     print("Raw ADC Value: ", chan.value)
#     print("ADC Voltage: " + str(chan.voltage) + "V")
#     time.sleep(0.5)

interval_gust = 5 # gust measurement interval (in seconds)
interval_wind = 30 # wind measurement interval (in seconds)

# make binary readout
# digital inputs are 128, 65472 and occasionally some intermediates
def spin(value):
    if(value == 65472):
        return 1
    else:
        return 0

# get spin frequency (in Hz)
def spin_frequency(interval):
    wind_count = 0 # spin counter
    spin_prev = 0 # signal change 
    t_end = time.time() + interval # time window
    while time.time() < t_end:
        
        # detect signal change
        if(spin_prev != spin(chan.value)): # two changes for 1 pulse!
            wind_count = wind_count + 1
            spin_prev = spin(chan.value)

    # NEED ADDITIONAL CALIBRATION (use fixed number of rotations)
    return(wind_count / interval / 2)

# convert frequency to kmh
def convert_to_kmh(frequency):
    # m/s = Hz * 0.34 (from sensor documentation)
    # kmh = m/s * 3.6
    kmh = frequency * 0.34 * 3.6
    return(kmh)

# get wind and gust speed
def get_wind_speed(interval_wind, interval_gust):
    gust_speeds = []
    t_end = time.time() + interval_wind # define time window
    while time.time() < t_end:
        gust_speed = convert_to_kmh(spin_frequency(interval_gust))
        gust_speed = round(gust_speed, 1)
        print(datetime.datetime.now().time())
        print(str(interval_gust) + "s speed: " + str(gust_speed) + " km/h")
        gust_speeds.append(gust_speed)
    
    # wind as average of gusts
    wind_average = statistics.mean(gust_speeds)

    # gusts as max
    wind_gust = max(gust_speeds)

    # return vector: average wind in kmh, gusts in kmh
    return([wind_average, wind_gust])

wind_speed = get_wind_speed(interval_wind, interval_gust)
print(str(interval_wind) + "s summary:")
print("Wind speed: " + str(round(wind_speed[0], 1)) + " km/h")
print("Gust speed: " + str(round(wind_speed[1], 1)) + " km/h")