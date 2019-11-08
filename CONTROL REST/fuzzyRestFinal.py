import time
import board
import busio
import adafruit_mcp4725
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

def Fuzzy():
    quality = ctrl.Antecedent(np.arange(0, 11, 1),'quality')
    service = ctrl.Antecedent(np.arange(0, 11, 1),'service')
    tip = ctrl.Consequent(np.arange(0, 26, 1),'tip')

    #Auto-membership functions population
    quality.automf(3)
    service.automf(3)

    tip['low'] = fuzzy.trimf(tip.universe, [0, 0, 13])
    tip['medium'] = fuzzy.trimf(tip.universe, [0, 13, 25])
    tip['high'] = fuzzy.trimf(tip.universe, [13, 25, 25])

    #Define RULES
    rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
    rule2 = ctrl.Rule(service['average'], tip['medium'])
    rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
    return tipping

def fuzzy_control(tipping, qual, serv):
    tipping.input['quality'] = qual 
    tipping.input['service'] = serv
    tipping.compute()
    return tipping.output['tip']

def adc_converter(chan1, chan2):
    v1 = chan1.voltage #0to3.3V
    v2 = chan2.voltage #0to3.3V
    return np.minimum(10,(v1*10/3.3)) , np.minimum(10,(v2*10/3.3)) 

def dac_converter(u):
    #Definimos que 0 a 25 sera 0 a 1
    #Pero la salida es de 0-3.3 es 0-4095
    u_scalebin = np.divide((u*4095),(25*3.3))
    u_scalevolt = np.divide(u,25)
    u_bin = np.int(np.maximum(0,np.minimum(4095,u_scalebin)))
    u_volt = np.maximum(0,np.minimum(1,u_scalevolt))
    return u_volt, u_bin
    

if __name__=="__main__":
    start = time.time()
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c, address = 0x48)
    dac = adafruit_mcp4725.MCP4725(i2c)
    fuzzySistem = Fuzzy()
    #Create single-ended input on channel 0
    chan1 = AnalogIn(ads, ADS.P0)
    chan2 = AnalogIn(ads, ADS.P1)
    chan3 = AnalogIn(ads, ADS.P2)
   
    while True:
        qual, serv = adc_converter(chan1, chan2)
        u = fuzzy_control(fuzzySistem, qual, serv)
        u_volt, u_bin = dac_converter(u)
        dac.raw_value = u_bin
        u_readV = chan3.voltage
        print('Quality:',qual)
        print('Service:',serv)
        print('Fuzzy Output:',u)
        print('Output Voltage:',u_volt)
        print('Output Volt_Read:',u_readV)
        dt = time.time() - start
        print('Time: '+str(dt))
        print(' ')
        time.sleep(0.5)
        start = time.time()

