import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import fmin
from scipy import interpolate

## inlet pressure

def inletP(t) :
    Ampli = 40 #mmHg
    Base = 80 #mmHg
    Tc = 0.2 #contraction phase
    Tr = 0.7 #relaxation phase
    
    modt = t%1

    if(0<= modt and modt <= Tc) :
        return Base + Ampli * 0.5 * (1 - np.cos(np.pi * modt / Tc) )
    elif(Tc < modt <= Tc + Tr) :
        return Base + Ampli * 0.5 * (1 + np.cos(np.pi * (modt-Tc) / Tr) )
    else :
        return Base


## Modele RCR
# Pin - P = Rp Qin
# P - outP = Rd Qout
# C dP = Qin - Qout
# dP = (Pin - P)/(C*Rp) - (P - Pout)/(C*Rd) --> Pin et Pout sont supposees connues, Pin avec la fonction inletP et Pout = constante

def modelRCR(y,t, Rp, Rd, C) :
    outletP = 5 #mmHg
    dP = (inletP(t) - y)/(Rp*C) - (y - outletP)/(Rd*C)
    return dP


#Resolution du modele RCR

#Paramètres
Rp = 50    #Resistance, blood viscosity
Rd = 100
C = 1e-3   #Capacitance, wall compliance


time = np.arange(0, 10, 0.01)

#initial pressure
X0 = 30
yrcr = odeint(modelRCR, X0, time, args=(Rp, Rd, C))

#relance avec une nouvelle condiction initiale (basee sur la solution precedente) -> permet d'avoir la solution periodique plus rapidement
y0 = yrcr[-1,0]
y2 = odeint(modelRCR, y0, time, args=(Rp, Rd, C))


# calcul du flux d'entrée
def computeQ(time, P, param) : 
    Qin = np.zeros(len(time))
    for i in range(len(time)) : 
        Qin[i] = (inletP(time[i]) - P[i])/param
    return Qin

Qin = computeQ(time, y2[:,0], Rp) 
plt.plot(time, Qin, label = 'Qin model RCR')
plt.legend()


## Donnee synthetique
Tper = 101 # 1s = 1per = 100 index
Q = Qin[-Tper:] # dernière periode
tt = time[-Tper:] - time[-Tper] # temps de la dernière periode
Q_bruit = Q + 0.01*np.random.randn(len(Q)) #ajout du bruit

plt.figure()
plt.plot(tt, Q, '-', label = 'donnee')
plt.plot(tt, Q_bruit, 'x', label = 'donnee bruitee')
plt.legend()
plt.show()


## definition d'une distance, on suppose la condition initiale connue
def dist(param, x0, obs, t) :
    Rp, Rd, C = param

    model = odeint(modelRCR, x0, t, args=(Rp, Rd, C))
    #calcul Q en entree car c'est ce qui est observé
    Qmod = computeQ(t, model[:,0], Rp)
    
    return( np.sum( (Qmod[:] - obs[:])**2 ) )


## estimation des parametres du RCR
# init
Rp0 = 10
Rd0 = 20
C0= 0.01
#optimisation
opt = fmin(dist, [Rp0, Rd0, C0], args = (y0, Q_bruit, tt)) # minimisation
print('param opt = ', opt)
print('vrai param = ', [Rp, Rd, C])

#comparaison model / donnee synthetique
yfit = odeint(modelRCR, y0, tt, args=(opt[0], opt[1], opt[2]))
Qfit = computeQ(tt, yfit[:, 0], opt[0])

plt.figure()
plt.plot(tt, Qfit, '-', label = 'model fit')
plt.plot(tt, Q, 'x', label = 'donnee syth')
plt.legend()
plt.show()


## donnee experimentale
Pdata = np.loadtxt('PressionAnim1.txt', skiprows=1)

tP = Pdata[:,0]
Pobs = Pdata[:,1]

interpP1 = interpolate.interp1d(tP, Pobs)

def expP(t) :  
    return( interpP1(t%tP[-1]) )
    
def RCR(y, t, Rp, Rd, C) :
    outletP = 0 #mmHg
    dP = (expP(t) - y)/(Rp*C) - (y - outletP)/(Rd*C)
    return dP

# calcul du flux d'entrée
def QfromP(time, P, param) : 
    Qin = np.zeros(len(time))
    for i in range(len(time)) : 
        Qin[i] = (expP(time[i]) - P[i])/param
    return Qin

def dist2(param, x0, obs, t) :
    Rp, Rd, C = param

    model = odeint(RCR, x0, t, args=(Rp, Rd, C))
    #calcul Q en entree car c'est ce qui est observé
    Qmod = QfromP(t, model[:,0], Rp)
    
    return( np.sum( (Qmod[:] - obs[:])**2 ) )


obs = np.loadtxt('FlowAnim1.txt', skiprows=1)
tobs = obs[:,0]
Qobs = obs[:,1]

plt.figure()
plt.plot(tobs, Qobs)

#test
Rp = 100.0
Rd = 1000.
C = 9e-4
p0 = 25.3

#optimisation
opt2 = fmin(dist2, [Rp, Rd, C], args = (p0, Qobs, tobs)) # minimisation
print('param opt = ', opt2)

#comparaison model / donnee synthetique
yfit = odeint(RCR, p0, tobs, args=(opt2[0], opt2[1], opt2[2]))
Qfit = QfromP(tobs, yfit[:, 0], opt2[0])

plt.figure()
plt.plot(tobs, Qfit, '-', label = 'model fit')
plt.plot(tobs, Qobs, 'x', label = 'donnee')
plt.legend()
plt.show()

