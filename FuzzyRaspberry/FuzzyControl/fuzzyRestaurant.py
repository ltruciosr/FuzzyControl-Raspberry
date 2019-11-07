import RPi.GPIO as GPIO
import smbus
import time
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

GPIO.setmode(GPIO.BCM)
bus = smbus.SMBus(1)

GPIO.setup( 4, GPIO.OUT) # bad service
GPIO.setup(17, GPIO.OUT) # good service

GPIO.output( 4, GPIO.LOW)
GPIO.output(17, GPIO.LOW)

def setup(Addr):
    global address
    address = 0x48

def read(chn):
    try:
        if chn == 0:
            bus.write_byte(address, 0x40)
        if chn == 1:
            bus.write_byte(address, 0x41)
        if chn == 2:
            bus.write_byte(address, 0x42)
        if chn == 3:
            bus.write_byte(address, 0x43)

        bus.read_byte(address)

    except Exception, e:
        print "Address: %s" % address
        print e

    return bus.read_byte(address)

def fuzzy():
    quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
    tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

    #Auto-membership functions population
    quality.automf(3)
    service.automf(3)

    tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
    tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
    tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

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

def ledOn(u):
    if u >= 0 and u < 13: # bad restaurant
        GPIO.output(17, GPIO.LOW)
        GPIO.output(4, GPIO.HIGH)

    elif u >= 13 and u < 26 : # good restaurant
        GPIO.output(4, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH)

    else:
        print 'strange value calculated'

if __name__ == "__main__":
    setup(0x48)
    start = time.time()
    fuzzySistem = fuzzy()
    while True:
        qual = int(read(0)/25)
        serv = int(read(1)/25)
        u = fuzzy_control(fuzzySistem, qual, serv)
        print 'calidad      = ', qual
        print 'servicio     = ', serv
        print 'Fuzzy Output = ', u
        ledOn(u)
        dt = time.time() - start
        #print 'Time = ', dt
        print ' '
        time.sleep(0.2)
        start = time.time()

