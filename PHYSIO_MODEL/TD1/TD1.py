import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.optimize import fmin

# function that returns dy/dt
def model(y,t):
    k = 0.3
    dydt = -k * y
    return dydt

# initial condition
y0 = 5

# time points
t = np.linspace(0,20)

# solve ODE
y = odeint(model,y0,t)

# plot results
plt.plot(t,y)
plt.xlabel('time')
plt.ylabel('y')
plt.title('Question 1')
plt.show()

def model2(y,t,k):
    dydt = -k * y
    return dydt

# solve ODEs
k = 0.1
y1 = odeint(model2,y0,t,args=(k,))
k = 0.2
y2 = odeint(model2,y0,t,args=(k,))
k = 0.5
y3 = odeint(model2,y0,t,args=(k,))
# plot results
plt.plot(t,y1,'r-',linewidth=2,label='k=0.1')
plt.plot(t,y2,'b--',linewidth=2,label='k=0.2')
plt.plot(t,y3,'g:',linewidth=2,label='k=0.5')
plt.xlabel('time')
plt.ylabel('y')
plt.legend()
plt.show()

## change init condition
# solve ODEs
k = 0.1
y0 = 2
y1 = odeint(model2,y0,t,args=(k,))
y0 = 5
y2 = odeint(model2,y0,t,args=(k,))
y0 = 8
y3 = odeint(model2,y0,t,args=(k,))
# plot results
plt.plot(t,y1,'r-',linewidth=2,label='y0 =2')
plt.plot(t,y2,'b--',linewidth=2,label='y0=5')
plt.plot(t,y3,'g:',linewidth=2,label='y0=8')
plt.xlabel('time')
plt.ylabel('y')
plt.legend()
plt.show()

def model3(y,t,k):
    dydt = -k * y * y
    return dydt

# solve ODEs
k = 0.1
y1 = odeint(model3,y0,t,args=(k,))
yexact = 1 / (k*t + 1/y0)
# plot results
plt.plot(t,y1,'r-',linewidth=2,label='simu')
plt.plot(t,yexact,'k.',linewidth=2,label='exact')
plt.xlabel('time')
plt.ylabel('y')
plt.legend()
plt.show()


## 2D model
def model4(x,t):
    return [-x[0],-x[1]]

Y0 = [1, 5] # 2d initial condition
Y = odeint(model4,Y0,t)
# plot results
plt.plot(t,Y[:,0],'r-',linewidth=2,label='x0')
plt.plot(t,Y[:,1],'b--',linewidth=2,label='x1')
plt.xlabel('time')
plt.legend()
plt.show()

# time points
tt = np.linspace(0,10)

def model5(x,t):
    return [x[0]-x[1], x[1]-x[0]]

Y0 = [0.002, 0.005]
Y = odeint(model5,Y0,tt)
# plot results
plt.plot(tt,Y[:,0],'r-',linewidth=2,label='A')
plt.plot(tt,Y[:,1],'b--',linewidth=2,label='B')
plt.xlabel('time')
plt.legend()
plt.show()

##--- Lotka-Volterra model
def LV(x,t, r, mu, rho, lam):
    dAdt = r*x[0] - mu*x[0]*x[1]
    dBdt = rho*x[0]*x[1] - lam*x[1]
    return [dAdt, dBdt]

Y0 = [10, 5]

r = 1.0
mu = 0.1
rho = 0.075
lam = 1.5

tt = np.arange(0,20, 0.1) 
Y = odeint(LV,Y0,tt,args=(r,mu,rho,lam))
# plot results
plt.plot(tt,Y[:,0],'r-',linewidth=2, label='A')
plt.plot(tt,Y[:,1],'b--',linewidth=2, label='B')
plt.xlabel('time')
plt.legend()
plt.show()

#print max / min
print("max prey : ",max(Y[:,0]))
print("min prey : ",min(Y[:,0]))

print("max predator : ",max(Y[:,1]))
print("min predator : ",min(Y[:,1]))

# bonus : finding the period 
thr = max(Y[:,0]) * 0.9 # we take 90% of the max of the preys 
above_thr = np.where(Y[:,0]>thr)[0] # indices above the threshold
print(above_thr)
rabove = np.diff(above_thr) # tricks to find jumps 
jumps = np.where(rabove > 1)[0] # jumps are where the diff is > 1

# for each jump we note the start and its end 
start = above_thr[0]
events = []
for jump in jumps:
    end = above_thr[jump]
    events.append([start, end])
    start = above_thr[jump + 1] # the next start is a the next indice 
events.append([start, above_thr[-1]]) # do not forget the last 

# compute peak times - converting indexs to time values
peak_times = []
for event in events:
    start, end = event
    start_t, end_t = tt[start], tt[end]
    peak_times.append((end_t + start_t) /2) # we take the middle time 
# peaks times are where the peak is reached

# plot results
plt.plot(tt,Y[:,0],'r-',linewidth=2, label='A')
plt.plot(tt,Y[:,1],'b--',linewidth=2, label='B')
plt.plot(peak_times, max(Y[:,0])*np.ones(len(peak_times)), 'o', color = 'k')
plt.xlabel('time')
plt.legend()
plt.show()

# the average diff is the period 
period = np.mean(np.diff(np.array(peak_times)))
print(period)


##--  SIR model
def f_SIR(y, t, alpha, beta):
    # y=[S,I]
    S=y[0]
    I=y[1]
    dy=[-beta*S*I,beta*S*I-alpha*I,alpha*I]
    return dy
S0 = 0.9
I0 = 0.1
R0 = 0

y0=[S0, I0, R0]

alpha=0.1
beta=0.25

Tmax=100
Nbt=1000
temps=np.linspace(0,Tmax,Nbt)

sol=odeint(f_SIR,y0,temps,args=(alpha,beta))
plt.subplot(1,2,1)
plt.plot(temps,sol)
plt.legend(['S(t)','I(t)','R(t)'])
plt.xlabel('t')
plt.title('modèle SIR alpha={} beta={}'.format(alpha,beta))

#with different parameters :

alpha=0.3
beta=0.2

sol=odeint(f_SIR,y0,temps,args=(alpha,beta))
plt.subplot(1,2,2)
plt.plot(temps,sol)
plt.legend(['S(t)','I(t)','R(t)'])
plt.xlabel('t')
plt.title('modèle SIR alpha={} beta={}'.format(alpha,beta))


##--  Chaotic Attractor Lorentz
#The Lorenz attractor is a set of chaotic solutions of the Lorenz system.
#From Lorenz attractor commes the known "butterfly effect"
# If we do not have a perfect knowledge of the initial conditions we cannot predict the future course
# like the minuscule disturbance of the air due to a butterfly flapping its wings
# see last simulation as an illustration

def lorenz_system(current_state, t, para):
    # define the lorenz system
    # positions of x, y, z in space at the current time point
    x, y, z = current_state
    sigma, beta, rho = para
    # define the 3 ordinary differential equations known as the lorenz equations
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    
    # return a list of the equations that describe the system
    return [dx_dt, dy_dt, dz_dt]

# define the time points to solve for, evenly spaced between the start and end times
start_time  = 0
end_time    = 100
time_points = np.linspace(start_time, end_time, end_time*100)

# system parameters sigma, rho, and beta
para1 = (10.,8./3.,28.)

initial_state = np.array([1, 0, 0])

xyz = odeint(lorenz_system,initial_state, time_points ,(para1,))
# extract the individual arrays of x, y, and z values from the array of arrays
x = xyz[:, 0]
y = xyz[:, 1]
z = xyz[:, 2]

# plot the lorenz attractor in three-dimensional phase space
fig = plt.figure(figsize=(12, 9))
ax = fig.gca(projection='3d')

ax.plot(x, y, z, color='g', alpha=0.7, linewidth=0.6)
ax.set_title('Lorenz attractor phase diagram')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# now plot two-dimensional cuts of the three-dimensional phase space
fig, ax = plt.subplots(1, 3, sharex=False, sharey=False, figsize=(17, 6))

# plot the x values vs the y values
ax[0].plot(x, y, color='r', alpha=0.7, linewidth=0.3)
ax[0].set_title('x-y phase plane')

# plot the x values vs the z values
ax[1].plot(x, z, color='m', alpha=0.7, linewidth=0.3)
ax[1].set_title('x-z phase plane')

# plot the y values vs the z values
ax[2].plot(y, z, color='b', alpha=0.7, linewidth=0.3)
ax[2].set_title('y-z phase plane')

#Take (1, 0, 0) as initial conditions and (1+epsi, 0, 0) as another. Simulate the two trajectories over a period of time and plot the distance between the two
e = 1e-5
initial_state1 = np.array([1+e, 0, 0])
initial_state2 = np.array([1, 0, 0])

xyz1 = odeint(lorenz_system,initial_state1, time_points ,(para1,))
x1 = xyz1[:, 0]
y1 = xyz1[:, 1]
z1 = xyz1[:, 2]
xyz2 = odeint(lorenz_system,initial_state2, time_points ,(para1,))
x2 = xyz2[:, 0]
y2 = xyz2[:, 1]
z2 = xyz2[:, 2]

#compute the distance
dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2) 

#show the distance evolution with time
# with a very small difference of 1e-5 initialy, after some time we can see that the 2 solutions are very different (the distance increase). 

plt.figure()
plt.plot(time_points, dist) 
plt.show()

fig = plt.figure(figsize=(12, 9))
ax = fig.gca(projection='3d')

ax.plot(x1, y1, z1, color='g', alpha=0.7, linewidth=0.6)
ax.plot(x2, y2, z2, color='r', alpha=0.7, linewidth=0.6)

### --- Ajustement de données

data = np.fromfile('data.txt', sep='\n', dtype=float)
data = data.reshape((-1, 2))

##autre option
#data = np.loadtxt('data.txt') 

#print(data)

plt.figure()
plt.plot(data[:,0],data[:,1], 'o')
plt.xlabel('t')
plt.ylabel('y')

# you cannot apply directly the log since some data <0, so we keep only > 0 data points
logy = np.log(data[data[:,1]>0,1])
t =  data[data[:,1]>0,0]
plt.figure()
plt.plot(t,logy, 'o')
plt.xlabel('t')
plt.ylabel('log(y)')

# fit lineaire
## polyfit
# we search for a straight line so polynome degree = 1 
deg = 1

# we keep only the first point to improve the fit
p = np.polyfit(t[:7], logy[:7], deg) #p[0] : slope

#to find k by hand : we "read" on the graph
k=-0.6

# computation of the corresponding exponential functions
# the exponential function of the libary math do not support arrays, we use the expo function from numpy
yfit=np.exp(k*data[:,0]) # by hand
yfit1=np.exp(p[0]*data[:,0]) #with function polyfit

plt.figure()
plt.plot(data[:,0],yfit, label = 'k = -0.6')
plt.plot(data[:,0],yfit1, label = 'k = p[0]')
plt.plot(data[:,0],data[:,1],'o', label = 'data')
plt.legend()

## compute the distance
def dist(k):
    #load the data
    data = np.loadtxt('data.txt') 
    y = data[:,1]
    t = data[:,0]
    sse = np.sum( (y - np.exp(k * t))**2 )
    return sse

# print distance for the different values of k :
print("distance k=", k, " : ", dist(k))
print("distance k polyfit=", p[0], " : ", dist(p[0]))

## we minimize the distance with the Python function fmin
# help :  scipy.optimize.fmin(func, x0,args=(), xtol=0.0001, ftol=0.0001, maxiter=None, maxfun=None, full_output=0, disp=1, retall=0, callback=None, initial_simplex=None)
#Minimize a function using the downhill simplex algorithm.

kopt = fmin(dist, k)
yopt = np.exp(kopt * data[:,0]) # corresponding expo


plt.figure()
plt.plot(data[:,0],yopt, label = 'kopt')
plt.plot(data[:,0],data[:,1],'o', label = 'data')
plt.legend()

print("distance k opt (fmin) =", kopt, " : ", dist(kopt))

## assuming we approximate the data with a exponential function exp(-k * t), we find the value of k that minimize the chosen distance. Indeed the distance is smaller than the one obtained with polyfit

# --- 2. noizy simulated data
def func(x, r, k) :
    return(x**r * np.exp(-k * x) )

# we choose r and k
k = 0.2
r = 2
# creat synthetic data (first no noise)
N = 100
x = np.linspace(0, 10, N)
donnee = func(x, r, k)

## add a noise
sigm = 0.3 # noise level
noisy_data =  donnee + np.random.randn(N)*sigm # noisy synthetic data

#definition of the distance to minimize
def chi2(rk, x, data) :# data and x need to have the same length
    r, k = rk
    ymodel = func(x, r, k)
    sse = np.sum( (ymodel - data)**2 )
    return sse

## estimation of r and k :
rk0 = [1, 1] # initial guess
rkopt1 = fmin(chi2, rk0, args = (x, noisy_data))
print(rkopt1)
#error with respect to the true value of each parameter
print("relative error of r: ", 100* np.abs(rkopt1[0] - r) / r )
print("relative error of k: ", 100* np.abs(rkopt1[1] - k) / k )

# fit results
plt.figure()
plt.plot(x, noisy_data, '.', label = 'noisy data')
plt.plot(x, func(x, rkopt1[0], rkopt1[1] ), label = 'model')
plt.legend()

## with various noise level : 
list_sigma = np.arange(0.01, 10, 0.5)
ropt_sig = []
kopt_sig = []
error = []
for sigma in list_sigma :
    noisy_data =  donnee + np.random.randn(N)*sigma
    rkopti = fmin(chi2, rk0, args = (x, noisy_data))
    ropt_sig.append(rkopti[0])
    kopt_sig.append(rkopti[1])
    #sum relativ error on r and k
    error.append(np.abs(rkopti[1] -k)/ k + np.abs(rkopti[0] -r)/ r) 

plt.figure()
plt.plot(list_sigma, error)
plt.xlabel('noise level')
plt.ylabel('relativ error')

## with various data vector size:
list_N = np.arange(2, 100, 10)
sigma = 0.3
kopt_N = []
ropt_N = []
error_N = []
for N in list_N :
    xN = np.linspace(0, 10, N)
    noisy_dataN =  func(xN,r, k) + np.random.randn(N)*sigma
    rkopti = fmin(chi2, rk0, args = (xN, noisy_dataN))
    ropt_N.append(rkopti[0])
    kopt_N.append(rkopti[1])
    error_N.append(np.abs(rkopti[1] -k)/ k + np.abs(rkopti[0] -r)/ r)
    
plt.figure()
plt.plot(list_N, error_N)
plt.xlabel('N : number of data')
plt.ylabel('relativ error')

plt.show()
