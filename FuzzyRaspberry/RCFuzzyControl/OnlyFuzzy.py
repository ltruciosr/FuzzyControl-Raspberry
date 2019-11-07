import time
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
if __name__=="__main__":
    start = time.time()
    fuzzySistem = Fuzzy()
    while True:
        qual, serv = 10*(np.random.random_sample((2,)))
        u = fuzzy_control(fuzzySistem, qual, serv)
        print('Fuzzy Output: '+str(u))
        dt = time.time() - start
        print('Time: '+str(dt))
        print(' ')
        time.sleep(1)
        start = time.time()

