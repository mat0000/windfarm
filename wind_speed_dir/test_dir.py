#!/usr/bin/python

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import psycopg2
from config import config
import time
import numpy
import smbus


bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
lsb = 0.012890625

def direction_voltage():
    adc = bus.read_i2c_block_data(DEVICE_ADDRESS, 0, 3)
    return(adc[2] * lsb) ### + lsb can be added

# setup 
interval_gust = 20 # gust measurement interval (in seconds)
interval_wind = 60 # wind measurement interval (in seconds)
interval_lag = 10 # readout interval

lag_speeds = []
lag_directions = []
def get_gust_speed_direction():
    
    t_end = time.time() + interval_gust # time window
    while time.time() < t_end:

        # detect wind direction
        print('Direction voltage: ' + str(direction_voltage()))
        time.sleep(0.5)

get_gust_speed_direction()

    