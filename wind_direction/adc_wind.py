#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
lsb = 0.012890625

def direction_voltage():
	adc=bus.read_byte_data(DEVICE_ADDRESS, 0)
	return adc

while True:
	print(str(direction_voltage()), "V")
	time.sleep(1)

