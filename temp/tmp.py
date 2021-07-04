#!/usr/bin/python
# -*- coding:utf-8 -*-
import smbus
import time

address = 0x20

bus = smbus.SMBus(1)
while True:
    us.write_byte(address,0xEF)
    ime.sleep(0.5)
    us.write_byte(address,0xFF)
time.sleep(0.5)
