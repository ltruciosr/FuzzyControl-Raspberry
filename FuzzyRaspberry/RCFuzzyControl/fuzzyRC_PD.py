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
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c, address = 0x48)
    dac = adafruit_mcp4725.MCP4725(i2c)
    fuzzySistem = Fuzzy()
    #Create single-ended input on channel 0
    chan1 = AnalogIn(ads, ADS.P0)
    chan2 = AnalogIn(ads, ADS.P1)
    chan3 = AnalogIn(ads, ADS.P2)
    dac.raw_value = 0
    print('Inicializando, wait 10 seconds')
    time.sleep(10)
    start = time.time()
    

    while True:
        #qual, serv = adc_converter(chan1, chan1)
        #u = fuzzy_control(fuzzySistem, qual, serv)
        # 3.3 represent 1 voltio de salida
        u = (chan1.voltage/3.3)
        u_volt, u_bin = dac_converter(25*u)
        dac.raw_value = u_bin
        #print('Quality:',qual)
        #print('Service:',serv)
        print('Voltage Input:','{0: .2f}'.format(u))
        #print('Voltage Input Circuit:','{0: .2f}'.format(chan2.voltage))
        print('Voltage Output:','{0: .2f}'.format(chan3.voltage))
        dt = time.time() - start
        #print('Time: '+str(dt))
        print(' ')
        time.sleep(0.1)
        start = time.time()

