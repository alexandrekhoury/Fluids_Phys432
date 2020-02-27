# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:04:27 2020

@author: Alexandre Khoury

Worked with : 
    Ronan Legin and Mathieu Bruneault
"""



import numpy as np
import matplotlib.pyplot as plt

#initiating conditions

dx=1
tmax=500000

#velocity
u=-0.1

#dt < dx/u
#stability condition
dt=dx/20

#grid size
nsize=1000

#defining x
x=np.arange(0,nsize)

#defining function for the FTCS method
f1_temp=np.ones(nsize)
f1_temp=x*f1_temp

#defining function for the Lax-Friedrich method
f2_temp=np.ones(nsize)
f2_temp=x*f2_temp


#for the plots
plt.ion()

fig, axes = plt.subplots(1,2)
axes[0].set_title('FTCS')
axes[1].set_title('Lax-Friedrich')
x1, = axes[0].plot(x,f1_temp)
x2, = axes[1].plot(x,f2_temp)

x1.set_ydata(f1_temp)
x2.set_ydata(f2_temp)

fig.canvas.draw()

for t in range(0,tmax):
    
    #implementing equation 8 (FTCS)
    f1_temp[1:-1]=f1_temp[1:-1]-u*dt/(2*dx)*(f1_temp[2:]-f1_temp[:-2])
    #implementing equation 11 (Lax)
    f2_temp[1:-1]=1/2*(f2_temp[2:]+f2_temp[:-2])-u*dt/(2*dx)*(f2_temp[2:]-f2_temp[:-2])
    
    #plotting the solutions at every 1000 time steps 
    if t%1000==0:
        
        x1.set_ydata(f1_temp)
        x2.set_ydata(f2_temp)
        fig.canvas.draw()
        plt.pause(0.001)
