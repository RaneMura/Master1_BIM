import numpy as np
from scipy import interpolate

Pdata = np.loadtxt('PressionAnim1.txt', skiprows=1)

tP = Pdata[:,0]
Pobs = Pdata[:,1]

interpP1 = interpolate.interp1d(tP, Pobs)

def expP(t) :  
    return( interpP1(t%tP[-1]) )
