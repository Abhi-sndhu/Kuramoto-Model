import numpy as np
import matplotlib.pyplot as plt

#Parameters
N= 200 #No. of oscillators 
K=5 #Coupling strength
thetai=np.random.uniform(0,2*np.pi,N) #Initiate random phases (0 to 2pi), Gaussian distribution
#thetai=np.random.standard_cauchy(N) #lorentzian distribution
omegai=np.random.normal(0,1,N) #Gaussian distribution with 0 as mean, 1 as standard deviation
dt=0.05

#Plot
plt.ion()
fig,ax = plt.subplots()
sc = ax.scatter(np.cos(thetai), np.sin(thetai))
ax.set_xlim(-1.2,1.2)
ax.set_ylim(-1.2,1.2)
ax.set_aspect('equal')

ax.set_xlabel("cos(theta)")
ax.set_ylabel("sin(theta)")
ax.set_title("Simulation of Synchronization")


def sigma(thetai):
  sigma_sin_diff_i=[]
  for i in range(N):
    summ=0
    for j in range (N):
      summ+= np.sin(thetai[j]-thetai[i]) 
    sigma_sin_diff_i.append(summ)
  return(sigma_sin_diff_i)

def order(thetai):
  z = np.mean(np.exp(1j * thetai))   # complex order parameter
  r = np.abs(z)                     # coherence
  psi = np.angle(z) 
  return(r,psi)   

#Update
def update(thetai,thetaidot):
  d_thetai= np.array(thetaidot)*dt 
  thetai=np.array(thetai)+d_thetai
  return (thetai)

def Kuramoto(K,thetai):
   Ts,rs=[],[]
   for steps in range(800):
     sigma_sin_diff_i= sigma(thetai)
     thetaidot=np.zeros(N)
     for i in range(N):
        thetaidot[i]= omegai[i] + (K*sigma_sin_diff_i[i])/N  #d thetai / dt = L, d thetai= L*dt
     thetai=update(thetai,thetaidot)
  
     Ts.append(steps)
     r,psi=order(thetai)
     rs.append(r)
     costheta=np.cos(thetai)
     sintheta=np.sin(thetai)
     sc.set_offsets(np.c_[costheta,sintheta])
     plt.draw()
     plt.pause(1e-10)   # real-time refresh
   return(Ts,rs)

Ts,rs= Kuramoto(5,thetai)  
plt.figure()
plt.xlabel('Time(t)')
plt.ylabel('Phase Coherence(r)')
plt.plot(Ts,rs)

rss=[]
Ks=[]
for i in np.arange(0,5.1,0.1):
  thetai=np.random.uniform(0,2*np.pi,N)
  #thetai=np.random.standard_cauchy(N) #lorentzian distribution
  Ts,rs=Kuramoto(i,thetai)
  Ks.append(i)
  rss.append(rs[-1])
plt.figure()
plt.xlabel('Coupling Strength(K)')
plt.ylabel('Phase Coherence(r)')
plt.plot(Ks,rss)
plt.show()
