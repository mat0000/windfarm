#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
lsb = 0.012890625

while True:
	adc=bus.read_byte_data(DEVICE_ADDRESS, 0)
	print(str(adc*lsb), "V")
	time.sleep(1)

