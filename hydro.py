# -*- coding: utf-8 -*-
"""

1-Dimensional Hydro solver

Created on Tue Feb 25 11:48:25 2020

@author: Alexandre Khoury

Worked with Ronan Legin
and Mathieu Bruneault
and Manuel Bolduc
"""

import numpy as np
import matplotlib.pyplot as plt

#defining a gaussian function
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

#setting up the parameters
dt=0.001
dx=1
tmax=50000
cs=50

#grid size
nsize=1000

#defining the intial density as a gaussian
x=np.arange(0,nsize)
f1=gaussian(x,nsize//2,nsize//10)*0.2+1
f1_temp=np.zeros(nsize)

f2=np.zeros(nsize)
f2_temp=np.zeros(nsize)
u=np.zeros(nsize-1)

#f2=u*f1 
f2[1:-1]=u[:1]*f1[1:-1]

#intializing the arrays for J
#note: I have used Jp and Jm to explicitly show the equations in the documents
#I could've however used only one array since they are almost the same
Jp_temp=np.zeros(nsize-1)
Jp1=np.zeros(nsize-1)
Jp2=np.zeros(nsize-1)

Jm_temp=np.zeros(nsize-1)
Jm1=np.zeros(nsize-1)
Jm2=np.zeros(nsize-1)

# plots 

x=np.arange(0,nsize)
plt.ion()

fig, axes = plt.subplots(1,2)
axes[0].set_title('Density')
axes[1].set_title('Velocity')
x1, = axes[0].plot(f1)
x2, = axes[1].plot(u)
plt.ylim(0,4)
x1.set_ydata(f1)
plt.ylim(-np.max(u)*1.2,np.max(u)*1.2)
x2.set_ydata(u)

fig.canvas.draw()




for t in range (0,tmax):
    
    #defining the velocity as shown
    u[1:]=1/2*(f2[1:-1]/f1[1:-1]+f2[2:]/f1[2:])
    u[0]=1/2*(f2[0]/f1[0]+f2[1]/f1[1])
    
    #instead of doing an if condition, find where velocity is positive and negative
    indices1=np.array(np.where(u[1:]>0))+1
    indices2=np.array(np.where(u[1:]<0))+1
    
    indices3=np.array(np.where(u[:-1]>0))
    indices4=np.array(np.where(u[:-1]<0))
    
    #implementing the good equation at the times where the velocity works
    Jp_temp[1:]=u[1:]*f1[1:-1]
    Jp1[indices1]=Jp_temp[indices1]
    
    Jp_temp[1:]=u[1:]*f1[2:]
    Jp1[indices2]=Jp_temp[indices2]
    
        
    Jm_temp[:-1] =u[:-1]*f1[:-2]
    Jm1[indices3]=Jm_temp[indices3]    
    
    Jm_temp[:-1] = u[:-1]*f1[1:-1]
    Jm1[indices4]=Jm_temp[indices4]
    
    #updating f1
    f1_temp[1:-1]=f1[1:-1]-dt/dx*(Jp1[1:]-Jm1[:-1])
    f1[1:-1]=f1_temp[1:-1]
    
    
    #boundary conditions for f1
    
    f1[0]= f1[0]-dt/dx*(Jm1[0])
    f1[-1]=f1[-1]+dt/dx*(Jp1[-1])
    
    #boundary end
    
    #repeat the process for f2 (same equations and same method)
    
    Jp_temp[1:]=u[1:]*f2[1:-1]
    Jp2[indices1]=Jp_temp[indices1]
    
    Jp_temp[1:]=u[1:]*f2[2:]
    Jp2[indices2]=Jp_temp[indices2]
    
        
    Jm_temp[:-1] =u[:-1]*f2[:-2]
    Jm2[indices3]=Jm_temp[indices3]
    
    Jm_temp[:-1] = u[:-1]*f2[1:-1]
    Jm2[indices4]=Jm_temp[indices4]
    
    
    #updating f2
    f2_temp[1:-1]=f2[1:-1]-dt/dx*(Jp2[1:]-Jm2[:-1])
    
    #adding source term for f2
    f2[1:-1]=f2_temp[1:-1]-dt/dx*cs**2*(f1[2:]-f1[:-2])
    
    #boundary conditions for f2
    
    f2[0]=f2[0]-dt/dx*(Jm2[0])
    f2[-1]=f2[-1]+dt/dx*(Jp2[-1])
    
    #plotting every 100 time steps
    
    if t%100==0:
    
        
        x1.set_ydata(f1)
        plt.ylim(-np.max(u)*1.2,np.max(u)*1.2)
        x2.set_ydata(u)
        
        fig.canvas.draw()
        plt.pause(0.001)
        
        
        
    

    
    
