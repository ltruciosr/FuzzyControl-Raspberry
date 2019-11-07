import board
import busio
import adafruit_mcp4725
import time

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

while True:
    # Go up the 12-bit raw range.
    print('Going up 0-3.3V...')
    for i in range(40):
        volt = i*100
        print(volt)
        dac.raw_value = volt
        time.sleep(1)
