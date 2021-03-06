#!/usr/bin/python

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import psycopg2
from config import config
import time
import datetime
import math
import numpy
import smbus
from gpiozero import Button

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
lsb = 0.012890625

def direction_voltage():
    adc = bus.read_i2c_block_data(DEVICE_ADDRESS, 0, 3)
    return(adc[2] * lsb) ### + lsb can be added

# chan_speed = AnalogIn(mcp, MCP.P2)
chan_speed = Button(17)
wind_count = 0

# setup 
interval_gust = 20 # gust measurement interval (in seconds)
interval_wind = 60 # wind measurement interval (in seconds)

# map volt: angle 
volts = {2.5: 0, 1.5: 45, 0.3: 90, 0.6: 135, 0.9: 180, 2.0: 225, 3.0: 270, 2.9: 315}

# map angle: direction
directions_name = {0: "NE", 45: "E", 90: "SE", 135: "S", 180: "SW", 225: "W", 270: "NW", 315: "N"}

# function to get average angle (in degrees)
def get_average(angles):
    
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    if(len(angles) == 0):
        return float("nan")
    else:
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
    

def spin():
    # two counts per single spin. 
    global wind_count
    wind_count = wind_count + 1

# function to convert frequency to kmh
def convert_to_kmh(frequency):
    # m/s = Hz * 0.34 (from sensor documentation)
    # kmh = m/s * 3.6
    kmh = frequency * 0.34 * 3.6
    return(kmh)

# function to get wind speed (in kmh) and angle (degrees)
# short term readout (using interval_gust timw window)
def get_gust_speed_direction():
    global wind_count
    wind_count = 0 # spin counter
    directions = [] # directions vector
    t_end = time.time() + interval_gust # time window
    while time.time() < t_end:
        
        # detect wind speed
        chan_speed.when_pressed = spin
        
        # detect wind direction
        d_direction = round(direction_voltage(), 1)
        if d_direction in volts:
            directions.append(volts[d_direction])
        time.sleep(0.001)

    # NEED ADDITIONAL CALIBRATION (use fixed number of rotations)
    spin_frequency = wind_count / interval_gust
    speed = round(convert_to_kmh(spin_frequency), 1)
    
    # average direction
    directions = [x for x in directions if math.isnan(x) == False]
    wind_direction = round(get_average(directions))
    return([speed, wind_direction])

# function to get wind and gust speed (in kmh) and wind direction (degrees)
def get_speed_dir():
    gust_speeds = []
    directions = []
    t_end = time.time() + interval_wind # define time window
    while time.time() < t_end:
        data = get_gust_speed_direction()
        gust_speeds.append(data[0])
        directions.append(data[1])

    # wind as average of gusts
    wind_speed = round(numpy.mean(gust_speeds), 1)

    # gusts as max gust speed
    gust_speed = max(gust_speeds)

    # wind direction as average angle over long time period
    wind_direction = round(get_average(directions))

    # time.sleep(0.5)
    # return vector: average wind speed, gust speed (kmh) and direction (angle)
    return([wind_speed, gust_speed, wind_direction])

# insert into DB
def insert_speed_gust_dir(time_cur, wind_speed, gust_speed, wind_direction):
    
    sql = """INSERT INTO wind (date, wind_speed, gust, direction_dg)
             VALUES(%s,%s,%s,%s);"""
    conn = None
    
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (time_cur, wind_speed, gust_speed, wind_direction))
        
        # commit the changes to the database
        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into mobile table")
        
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# collect data and insert into DB
print('Collecting data using ' + str(interval_wind) + 's time window...')

data = get_speed_dir()
wind_speed = data[0]
gust_speed = data[1]
wind_direction = data[2]
time_cur = datetime.datetime.now()
time_cur = time_cur - datetime.timedelta(microseconds=time_cur.microsecond)

print('Time stamp: ' + str(time_cur))
print('Wind speed: ' + str(wind_speed) + ' kmh.')
print('Gust speed: ' + str(gust_speed) + ' kmh.')

if wind_direction in directions_name:
    print('Wind direction: ' + str(wind_direction) + ' degrees (' + directions_name[wind_direction] + ')')
else:
    print('Wind direction: ' + str(wind_direction) + ' degrees.')

# insert into DB
# if __name__ == '__main__':
#     insert_speed_gust_dir(time_cur, wind_speed, gust_speed, wind_direction)
            