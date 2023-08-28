# -*- coding: utf-8 -*-
# Question: Q9b - rk4 et numba, moins de points enregistrés
# Nom: Dirk Stratmann

import numpy as np

from rk4 import rk4

from numba import njit
import time

########## CALCUL:
    
@njit
def rk4Numba(x, dx, y, deriv,params):
    """
      /*-----------------------------------------
      sous programme de resolution d'equations
      differentielles du premier ordre par
      la methode de Runge-Kutta d'ordre 4
      x = abscisse, une valeur scalaire, par exemple le temps
      dx = pas, par exemple le pas de temps
      y = valeurs des fonctions au temps t(i), c'est un tableau numpy de taille n
      avec n le nombre d'équations différentielles du 1er ordre
      
      rk4 renvoie les nouvelles valeurs de y pour t(i+1)
      
      deriv = variable contenant le nom du
      sous-programme qui calcule les derivees
      deriv doit avoir trois arguments: deriv(x,y,params) et renvoyer 
      un tableau numpy dy de taille n 
      ----------------------------------------*/
    """
    #  /* d1, d2, d3, d4 = estimations des derivees
    #    yp = estimations intermediaires des fonctions */  
    ddx = dx/2.       #         /* demi-pas */
    d1 = deriv(x,y,params)   #       /* 1ere estimation */          
    yp = y + d1*ddx
    #    for  i in range(n):
    #        yp[i] = y[i] + d1[i]*ddx
    d2 = deriv(x+ddx,yp,params)     #/* 2eme estimat. (1/2 pas) */
    yp = y + d2*ddx    
    d3 = deriv(x+ddx,yp,params)  #/* 3eme estimat. (1/2 pas) */
    yp = y + d3*dx    
    d4 = deriv(x+dx,yp,params)     #  /* 4eme estimat. (1 pas) */
    #/* estimation de y pour le pas suivant en utilisant
    #  une moyenne ponderee des derivees en remarquant
    #  que : 1/6 + 1/3 + 1/3 + 1/6 = 1 */
    return y + dx*( d1 + 2*d2 + 2*d3 + d4 )/6  

@njit
def derivNumba(t, y, params):
    """
    Calcule les 1er dérivées de toutes les variables stockées dans y
    
    Parameters
    ----------
    t : un réel 
        le temps t actuel
    y : un tableau 1D numpy de dimension n, 
    avec n le nombre d'équations différentielles du premier ordre
        Contient les valeurs des n variables au temps t
    params : un scalaire ou un tableau
        Contient un ou des paramètres nécessaires pour le calcul

    Returns
    -------
    dy : même type que y
        Contient les 1er dérivées
    """
    
    omega = params
    dy = np.zeros(2)
    dy[0] = y[1]
    dy[1] = -omega**2*y[0]
    return dy

def deriv(t, y, params):
    """
    Calcule les 1er dérivées de toutes les variables stockées dans y
    
    Parameters
    ----------
    t : un réel 
        le temps t actuel
    y : un tableau 1D numpy de dimension n, 
    avec n le nombre d'équations différentielles du premier ordre
        Contient les valeurs des n variables au temps t
    params : un scalaire ou un tableau
        Contient un ou des paramètres nécessaires pour le calcul

    Returns
    -------
    dy : même type que y
        Contient les 1er dérivées
    """
    
    omega = params
    dy = np.zeros(2)
    dy[0] = y[1]
    dy[1] = -omega**2*y[0]
    return dy


def integrateODE(t, tmax, dt, saveInterval, init, deriv, params):
    
    tValues = np.arange(0, tmax, dt*saveInterval)
    nPoints = tValues.size
    xValues = np.empty(nPoints)
    
    n = init.size
    y = np.empty(n)
    y[:] = init # copy elements
    
    for i in range(nPoints):
        xValues[i] = y[0]
        t = tValues[i]
        for j in range(saveInterval):
            y = rk4(t, dt, y, deriv, params)
            t += dt

    return tValues, xValues

@njit
def integrateODE_numba(t, tmax, dt, saveInterval, init, deriv, params):
    
    tValues = np.arange(0, tmax, dt*saveInterval)
    nPoints = tValues.size
    xValues = np.empty(nPoints)
    
    n = init.size
    y = np.empty(n)
    y[:] = init # copy elements
    
    
    for i in range(nPoints):
        xValues[i] = y[0]
        t = tValues[i]
        for j in range(saveInterval):
            y = rk4Numba(t, dt, y, deriv, params)
            t += dt            
        
    return tValues, xValues



omega = 1
t = 0
dt = 0.001 
tmax = 1000 # assez grand pour voir un effet
saveInterval = 10 # n'enregistrer que tous les 10 points pour réduire la taille de la mémoire

# call it once before to force compilation 
# and to mesure time without the time needed for compilation
integrateODE_numba(t, 10, dt, saveInterval, np.array([1,0]), derivNumba, omega)

start = time.time()
integrateODE(t, tmax, dt, saveInterval, np.array([1,0]), deriv, omega)
end = time.time()
print("Standard python: %.2f s" % (end-start))

tmax *= 10
start = time.time()
integrateODE_numba(t, tmax, dt, saveInterval, np.array([1,0]), derivNumba, omega)
end = time.time()
print("With numba and tmax * 10: %.2f s" % (end-start))    

"""
prog9.py:
Results obtained on my machine:
Standard python: 13.58 s
With numba and tmax * 10: 5.86 s
So a 20 times faster exectution with numba
"""

"""
prog9b.py:
Results obtained on my machine:
Standard python: 13.36 s
With numba and tmax * 10: 5.87 s
So still a 20 times faster exectution with numba
and the absolute execution times are not affected, 
showing that the memory allocation is not important for execution time here
"""


