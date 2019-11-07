import time
import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

def Fuzzy():
    E = ctrl.Antecedent(np.arange(-1,2,2),'E')
    DE = ctrl.Antecedent(np.arange(-1,2,2),'DE')
    U = ctrl.Consequent(np.arange(-5,6,1),'U')

    #Auto-membership functions population
    names = ['N','P']
    E.automf(names = names)
    DE.automf(names = names)

    U['N'] = fuzzy.trimf(U.universe, [-5, -5, 0])
    U['Z'] = fuzzy.trimf(U.universe, [-5, 0, 5])
    U['P'] = fuzzy.trimf(U.universe, [0, 5, 5])

    #Define RULES
    rule1 = ctrl.Rule(E['N'] | DE['N'], U['N'])
    rule2 = ctrl.Rule(E['N'] | DE['P'], U['Z'])
    rule3 = ctrl.Rule(E['P'] | DE['N'], U['Z'])
    rule4 = ctrl.Rule(E['P'] | DE['P'], U['P'])

    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
    return tipping

def fuzzy_control(tipping, error, derror):
    tipping.input['E'] = error 
    tipping.input['DE'] = derror
    tipping.compute()
    return tipping.output['U']
if __name__=="__main__":
    start = time.time()
    fuzzySystem = Fuzzy()
    while True:
        error, derror= 2*(np.random.random_sample((2,)))-1
        u = fuzzy_control(fuzzySystem, error, derror)
        print('e:',error)
        print('de:',derror)
        print('Fuzzy Output:',u)
        dt = time.time() - start
        print('Time: '+str(dt))
        print(' ')
        time.sleep(2)
        start = time.time()
