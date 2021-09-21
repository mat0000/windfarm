#!/usr/bin/python

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import psycopg2
from config import config
import time

from gpiozero import Button

# chan_speed = AnalogIn(mcp, MCP.P2)
chan_speed = Button(17)
wind_count = 0

# setup 
interval_gust = 20 # gust measurement interval (in seconds)
interval_wind = 60 # wind measurement interval (in seconds)
interval_lag = 10 # readout interval

def spin():
    # two counts per single spin. 
    global wind_count
    wind_count = wind_count + 1
    print('Spin count: ' + str(wind_count))

lag_speeds = []
lag_directions = []
def get_gust_speed_direction():
    global wind_count
    wind_count = 0 # spin counter
    t_end = time.time() + interval_gust # time window
    while time.time() < t_end:
        
        # detect wind speed
        chan_speed.when_pressed = spin
        
get_gust_speed_direction()

    