import smbus
import time

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
lsb = 0.012890625

def direction_voltage():
	adc = bus.read_i2c_block_data(DEVICE_ADDRESS, 0, 3)
	return (adc[2] * lsb) ### + lsb can be added

while True:
	v = direction_voltage()
	with open('log.txt','a') as f:
		f.write(str(v) + '\n')
	print(str(v) + 'V')
	time.sleep(0.1)