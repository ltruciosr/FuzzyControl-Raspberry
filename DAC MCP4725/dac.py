import board
import busio
import adafruit_mcp4725

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725

while True:
    print('Going up')   #0to3.3V
    for i in range(4095):
        dac.raw_value = i
    print('Going down') #3.3Vto0
    for i in range(4095, -1, -1):
        dac.raw_value = i
