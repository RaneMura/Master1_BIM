
import numpy as np

def inletP(t) :
    Ampli = 40 #mmHg
    Base = 80 #mmHg
    Tc = 0.2 #contraction phase
    Tr = 0.7 #relaxation phase
    Per = 1 # HR in second
    
    modt = t%Per

    if(0<= modt and modt <= Tc) :
        return Base + Ampli * 0.5 * (1 - np.cos(np.pi * modt / Tc) )
    elif(Tc < modt <= Tc + Tr) :
        return Base + Ampli * 0.5 * (1 + np.cos(np.pi * (modt-Tc) / Tr) )
    else :
        return Base
