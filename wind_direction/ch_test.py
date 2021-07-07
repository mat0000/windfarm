import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan_direction = AnalogIn(mcp, MCP.P3)

while True:
    print('Voltage: ' + str(round(chan_direction.voltage, 2)))
    print('Value: ' + str(round(chan_direction.value, 2)))
    time.sleep(1)