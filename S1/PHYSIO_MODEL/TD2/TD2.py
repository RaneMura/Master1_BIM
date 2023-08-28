import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.optimize import fmin

## --------  Degradation d' un substrat de maniere standard
#eq diff qui gouverne l'evo de A, degradation d'un substrat
#dA/dt = -kA
#ce qui se resout explicitement: A(t) = A(0) exp(-k t)
#et numeriquement :
# function that returns dA/dt
def degradation(y,t,k):
    dydt = -k * y
    return dydt

# initial condition
y0 = 5

#vitesse de degradation k
k = 0.2

# time points
t = np.linspace(0,10,100)

# solve ODE
y = odeint(degradation,y0,t, args = (k,))


yexact = y0 * np.exp(-k * t)

# plot results
plt.plot(t,y, label = 'solution numérique')
plt.plot(t,yexact, '.', label = 'solution exacte')
plt.xlabel('time')
plt.ylabel('y')
plt.title('Degradation substrat')
plt.legend()

# mesures :
td = np.linspace(0,10,11)
Ad = [1.0,
      0.7952,
      0.3795,
      0.2960,
      0.3842,
      0.2343,
      0.3253,
      0.0511,
      0.0432,
      0.0224,
      0.0143]

#plot data
plt.figure()
plt.plot(td, Ad, 'o', label = 'donnees')

#temps demie vie : quand A/A0 = 0.5, ici A0 = 1.0 donc A/A0 = A
# avec les donnees t1/2 est autour de 2.0min
# or nous avons vu en cours que t1/2 = ln(2) / k

#ajustement sur les donnees : trouver le meilleur k
####------ option 0 : avec le cours
# t1/2 = 2 et t1/2 = ln(2) / k --> k = ln(2) / 2
kopt0 = np.log(2) / 2.

print('k ajusté avec le cours:', kopt0)
yajust0 = Ad[0] * np.exp(-kopt0 * t)
plt.plot(t, yajust0, label = 'sol ajustee avec le cours')

####------ option 1 : sol exacte
#definition de la distance à minimiser
def chi2(k, t, data) :# data and t need to have the same length
    ymodel = data[0] * np.exp(-k * t)
    sse = np.sum( (ymodel - data)**2 )
    return sse

# estimation de k :
k0 = 0.2 # initial guess
kopt1 = fmin(chi2, k0, args = (td, Ad)) # minimisation

print('k ajusté avec sol exacte:', kopt1)
yajust = Ad[0] * np.exp(-kopt1 * t)

plt.plot(t, yajust, label = 'sol ajustee avec sol exacte')

####------ option 2 : sol numérique
#definition de la distance à minimiser
def chi2bis(k, t, data) :# data and t need to have the same length
    ymodel = odeint(degradation,data[0],t, args = (k,))
    sse = np.sum( (ymodel - data)**2 )
    return sse

# estimation de k :
k0 = 0.2 # initial guess
kopt2 = fmin(chi2bis, k0, args = (td, Ad)) # minimisation

print('k ajusté avec sol numerique:', kopt2)
yajustbis = odeint(degradation,Ad[0],t, args = (kopt2,))
plt.plot(t, yajustbis, label = 'sol ajustee avec sol numerique')
plt.legend()
plt.show()


## --------  Reaction suicide
#-- 1. equations :
# dA/dt = -k*A*B
# dB/dt = -k*A*B

#-- 2. voir le cours :
#dA/dt - dB/dt = 0
#donc d(A-B)/dt = 0
#donc pout tout t,  A(t)-B(t) = constante
#donc poru tout t, B(t) = A(t) - constante et constante = A(0) - B(0)
#pour tout t, B(t) =  A(t) - (A(0) - B(0))

#-- 3. on en déduit que le systeme devient
# dA/dt = -k*A*( A - (A(0) - B(0)) )

#-- 4. resoudre
def ReacSuicide(y, t, k, A0, B0) :
    dAdt = -k*y*(y - (A0 - B0))
    return dAdt

A0 = 10.1
B0 = 8.0
k = 0.2
t = np.arange(0, 20.1, 0.1)

A = odeint(ReacSuicide, A0, t, args =(k, A0, B0))
#calcul B :
B = A - (A0 - B0)
plt.figure()
plt.plot(t, B, label = 'B')
plt.plot(t, A, label = 'A')

#-- 5. sol exacte :
C = B0 - A0
K = A0/B0
Aexacte = C * np.exp(-k*C*t) / (1./K - np.exp(-k*t*C) )
Bexacte = Aexacte - (A0 - B0)
plt.plot(t, Bexacte,'x', label = 'B exacte')
plt.plot(t, Aexacte,'x', label = 'A exacte')
plt.legend()


## --------  dimere : reaction A+A <-> B
B0 = 0 #que des monomeres au debut
A0 = 5.0
#-- 1. equations
#dA/dt = 2 * km1 * B - 2 * k1 * A*A 
#dB/dt = k1 * A*A - km1 * B

#-- 2. conservation
# dA/dt + 2dB/dt = 0 : la quantite A+2B est conservee (le nombre total de monomères est constant pour tout temps)
# en supposant B0 = 0 on obtient : A(t) + 2B(t) = A0

#-- 3. résolution numérique
k1 = 1.0
km1 = 1.0
def Polymeriz(y, t, k1, km1) :
    A,B = y
    dAdt = -2*k1 * A*A + 2*km1*B
    dBdt = -km1*B + k1*A*A
    return [dAdt, dBdt]

y0 = [A0, B0]
t =  np.arange(0, 10.1, 0.1)
y = odeint(Polymeriz, y0, t, args= (k1, km1,))

plt.plot(t, y)
plt.legend(['A', 'B'])

#-- 4. A l'équilibre
# on a dB*/dt = 0 : -km1 B* + k1 A*^2 = 0
# donc B* = (k1/km1) A*^2
# d'autre part, avec la conservation de masse (quest. 2), on a A* = A0 - 2B*
# en combinant les 2 informations on a : 
# B* = (k1/km1) A*^2 = (k1/km1) (A0 - 2B*)^2
# donc B* =  (k1/km1) (A0^2 - 4 A0 B* + 4 B*^2) 
# on obtient un polynome du second degré en B* : 4 (k1/km1) B*^2 - (4(k1/km1)A0 + 1) B* +  (k1/km1) A0^2 = 0
# on peut chercher les racines de ce polynome afin de trouver B* (qui dépendra de km1, k1 et A0). 


## --------  trimerisation : reaction A+A <-> B A+B <-> C
#-- 1. le systeme d'equation : 
# dAdt = -2*k1 * A*A + 2*km1*B + km2*C - k2 *B*A
# dBdt = -km1*B + k1*A*A - k2*A*B + km2*C
# dCdt = -km2*C + k2*A*B


#-- 2. à l'équilibre, A=A*, B = B*, C = C*
# d'une part :
# 0 = -2k1 A*^2 + 2km1 B* + km2 C* - k2 B* A*
# 0 = -km1 B* + k1 A*^2 - k2 A* B* + km2 C*
# 0 = -km2 C* + k2 A* B*
# de plus avec la conservation de masse : 
# A* + 2B* + 3C* = A0 (en supposant B0 = 0 et C0 = 0)
# (on a alors 3 inconnus A*, B* et C* et 4 équations)

#-- 3. resolution numerique

k1 = 1
km1 = 1
k2 =1
km2 =1

#que des monomeres au debut
A0 = 10
B0 = 0
C0 = 0

def Trimeriz(y, t, k1, km1, k2, km2) :
    A,B,C = y
    dAdt = -2*k1 * A*A + 2*km1*B + km2*C - k2 *B*A
    dBdt = -km1*B + k1*A*A - k2*A*B + km2*C
    dCdt = -km2*C + k2*A*B

    return [dAdt, dBdt, dCdt]

y0 = [A0, B0, C0]
t = np.linspace(0, 2)
#t =  np.arange(0, 2.1, 0.01)
y = odeint(Trimeriz, y0, t, args= (k1, km1,k2, km2))

plt.figure()

plt.plot(t, y)
plt.legend(['A', 'B', 'C'])


#-- 4. Pour avoir une trimerisation directe, il faut que le "passage par B" soit a vitesse très rapide par rapport aux autres reactions k2 = 15 par exemple

#- 5. resolusion si  la trimerization est "imediate" sans passer par B les complexes dimeres A+A+A <-> C

def Trimeriz2(X, t, k1, km1): 
    A,C = X
    dA = - 3 * k1 * A ** 3 + 3 * km1 * C
    dC = - km1 *C + k1 * A ** 3
    return  [dA, dC]

A0 = 10 
C0 =  0 
X0 = [A0,  C0]
k11 = 1
km11 = 1 

y2 = odeint(Trimeriz2, X0, t, args=(k11, km11,))

plt.figure()
plt.plot(t, y2, t, y)
plt.legend(['At', 'Ct', 'A', 'B', 'C']) # on remarque que rapidement le nombre de C est le meme


# ---- pour aller plus loin : 
# on trace le nombre de trimères à l'equi (on suppose qu'au temps final (grand) l'equilibre est atteint) en fonction du nombre initial de monomere
# faire varier les parametres pour faire correspondre les 2 courbes
#k1 = 1
#km1 = 0.1
#k2 = 10
#km2 =0.2

#k11 = 1
#km11 = 0.2 

#C1 = []
#C2 = []
#tlong =  np.arange(0, 20.1, 0.01)
#list_A0 = np.arange(1, 30, 2)
#for A0 in list_A0 :
#    y1 = odeint(Trimeriz, [A0, 0, 0], tlong, args= (k1, km1,k2, km2,))
#    y2 = odeint(Trimeriz2, [A0,0], tlong, args=(k11, km11,))
    # sauve l'equilibre
#    C1.append(y1[-1, 2])
#    C2.append(y2[-1, 1])

#trace le resultat :
#plt.figure()
#plt.plot(list_A0, C1, label = 'trim1')
#plt.plot(list_A0, C2, label = 'trim2')
#plt.legend()
#plt.show()



## --------  Réaction Ligant-Recepteur : L+R<-> R1 et I+R <-> R2
## ici on a un premier choix de modelisation d'un competiteur
def LigRecComp(X, t, k1, km1, k2, km2) :
    L, I, R, R1, R2 = X

    dL = -k1*L*R + km1*R1
    dI = -k2*I*R + km2*R2
    dR = -k1*L*R - k2*I*R + km1*R1 + km2 * R2
    dR1 = k1*L*R - km1*R1
    dR2 = k2*I*R - km2*R2
   
    return [dL, dI, dR, dR1, dR2]

# parameters et conditions initiales
L_0 = 10
R_0 = 20
I_0 = 1
R1_0 = 0
R2_0 = 0
X0 = [L_0, I_0, R_0, R1_0, R2_0]
k1 = 1
km1 = 1
k2 = 1
km2 = 1

#resoudre
t =  np.arange(0, 20.1, 0.01)
y = odeint(LigRecComp, X0, t, args=(k1, km1, k2, km2,))

#plot solutions
plt.figure()
plt.plot(t, y)
plt.legend(['L', 'I', 'R', 'R1', 'R2'])

#on suppose l'equilibre attein a la fin de la simu (il faut un temps suffisemment long)
Xeq = y[-1, :]
Leq = Xeq[0]
Ieq = Xeq[1]

# constance d'équilibre (cf cours)
kap1 = k1/km1
kap2 = k2/km2

R1_eq = R_0*kap1*Leq/(1 + kap1 *Leq + kap2*Ieq) # d' apres le cours
R2_eq = R_0*kap2*Ieq/(1 + kap1 *Leq + kap2*Ieq)

#on verifie les formules optenues dans le cours
plt.figure()
plt.plot(t, y[:,-2], label = 'R1')
plt.plot(t, R1_eq*np.ones(len(t)), '--', label = 'R1_eq')

plt.plot(t, y[:,-1], label = 'R2')
plt.plot(t, R2_eq*np.ones(len(t)), '--', label = 'R2_eq')
plt.legend()

## autre facon de modeliser un competiteur (plus besoin d'equation supplementaire)
#-- 3. On suppose I constant, (competiteur en grande quantité, toujours dispo)
# on a plus besoin de résoudre la partie avec I, pris en compte directement dans la vitesse de rencontre entre R et L
# pour simplifier je choisi : kappa + I = kap ici
# attention il faut modifier toutes les equations
def LigRecInib(X, t, k1, km1, kap) :
    L, R, R1 = X

    dL = -k1/kap *L*R + km1*R1
    dR = -k1/kap *L*R + km1*R1 
    dR1 = k1/kap *L*R - km1*R1
    
    return [dL, dR, dR1]

# parameters
L_0 = 10
R_0 = 20
R1_0 = 0

X0 = [L_0, R_0, R1_0]
k1 = 1
km1 = 1
kap = 3

#resoudre
t =  np.arange(0, 2.1, 0.01)
y2 = odeint(LigRecInib, X0, t, args=(k1, km1, kap,))
#with more I :
kap = 10
X0 = [L_0, R_0, R1_0]
y3 = odeint(LigRecInib, X0, t, args=(k1, km1, kap,))
#plot solutions
plt.figure()
plt.plot(t, y2)
plt.plot(t, y3, '--')
plt.legend(['L', 'R', 'R1','L2', 'R2', 'R1_2'])

## --------  Pathway simple ADN

def ADN(X, t, p, q, mu, r, lam, s):
    O, C, R, P = X
    dO = -p*O + q*C
    dC = p*O - q*C
    dR = -mu*R + r*O
    dP = -lam*P + s*R

    return [dO, dC, dR, dP]
#parameters
p = 0.3
q = 0.4
mu = 0.2
r = 0.2
lam = 0.1
s = 0.2

O_0 = 1
C_0 = 0
R_0 = 1
P_0 = 0
X0 = [O_0, C_0, R_0, P_0]
t =  np.arange(0, 100.1, 0.01)

X = odeint(ADN, X0, t, args=(p,q,mu,r,lam,s))
#plot solutions
plt.figure()
plt.subplot(2,2,1)
plt.plot(t, X[:,0], label = 'O')

plt.subplot(2,2,2)
plt.plot(t, X[:,1], label = 'C')

plt.subplot(2,2,3)
plt.plot(t, X[:,2], label = 'R')

plt.subplot(2,2,4)
plt.plot(t, X[:,3], label = 'P')

# la protéine inhibe sa propre expression : action sur l'ouverture de l'ADN
def ADN1(X, t, p, q, mu, r, lam, s, kap):
    O, C, R, P = X

    n = 10 # avec n grand on fait apparaitre des ocillations
    
    dO = -p*O + q/(kap+P**n)*C
    dC = p*O - q/(kap+P**n)*C
    dR = -mu*R + r*O
    dP = -lam*P + s*R

    return [dO, dC, dR, dP]

#suivant les valeurs de parametres choisi
#on peut faire apparaitre des comportements differents
kap = 0.05
X1 = odeint(ADN1, X0, t, args=(p,q,mu,r,lam,s, kap,))

#plot solutions
plt.subplot(2,2,1)
plt.plot(t, X1[:,0],'-.', label = 'O1')

plt.subplot(2,2,2)
plt.plot(t, X1[:,1],'-.', label = 'C1')

plt.subplot(2,2,3)
plt.plot(t, X1[:,2],'-.', label = 'R1')

plt.subplot(2,2,4)
plt.plot(t, X1[:,3],'-.', label = 'P1')

# la protéine inhibe sa propre expression : action sur la transcription
def ADN2(X, t, p, q, mu, r, lam, s, kap):
    O, C, R, P = X

    n = 10 # avec n grand on fait apparaitre des ocillations
    
    dO = -p*O + q*C
    dC = p*O - q*C
    dR = -mu*R + r/(kap+P**n) *O
    dP = -lam*P + s*R

    return [dO, dC, dR, dP]

X2 = odeint(ADN2, X0, t, args=(p,q,mu,r,lam,s, kap))
#plot solutions

plt.subplot(2,2,1)
plt.plot(t, X2[:,0],'--', label = 'O2')
plt.legend()

plt.subplot(2,2,2)
plt.plot(t, X2[:,1],'--', label = 'C2')
plt.legend()

plt.subplot(2,2,3)
plt.plot(t, X2[:,2],'--', label = 'R2')
plt.legend()

plt.subplot(2,2,4)
plt.plot(t, X2[:,3],'--', label = 'P2')
plt.legend()

plt.show()

