import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from onlyFuzzy import Fuzzy, fuzzy_control

# (3) ODE Integrator

fuzzySystem = Fuzzy()

def model(y ,t ,fuzzySystem, T):
    error = sp - y
    derror = error
    U = 5*fuzzy_control(fuzzySystem, error, derror)
    print('U',U,'error',error,'DE',derror)
    dydt = (U - y)/tau
    return dydt

sp = 0.7
tau = 1.5
T,n = 0.1,100
t = np.linspace(0,n*T, n+1)
y = odeint(model,0,t,args = (fuzzySystem, T))

    
plt.figure(1)
plt.plot(t,y,'b-',label=r'$\frac{dx}{dt}=3 \; \exp(-t)$')
plt.ylabel('response')
plt.xlabel('time')
plt.legend(loc='best')
plt.show()
