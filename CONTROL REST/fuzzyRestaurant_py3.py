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
    
    
    return
if __name__=="__main__":
    start = time.time()
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c, address = 0x48)
    dac = adafruit_mcp4725.MCP4725
    fuzzySistem = Fuzzy()
    #Create single-ended input on channel 0
    chan1 = AnalogIn(ads, ADS.P0)
    chan2 = AnalogIn(ads, ADS.P1)
    
    while True:
        qual, serv = adc_converter(chan1, chan2)
        print('Quality:',qual)
        print('Servicio:',serv)
        u = fuzzy_control(fuzzySistem, qual, serv)
        print('Fuzzy Output: '+str(u))
        dt = time.time() - start
        print('Time: '+str(dt))
        print(' ')
        time.sleep(2)
        start = time.time()
