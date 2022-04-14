# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 12:01:52 2021

@author: A90127
"""

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2Tk
from matplotlib.figure import Figure
#import matplotlib.animation as animation
#import tkinter.messagebox
#from tkinter import *
import tkinter as tk
from itertools import permutations


from DyesDataBuild import DyesDataBuild as DDB
Dyes = DDB(r'D:\A90127\DyingMath\data\spectrum_dye.xlsx')
from DyeMerge import SpecEst, Merge
from cieMath import Spec2LAB


def button_add():
    def surface(dye1,dye2):
        x = Dyes[dye1].conc
        y = Dyes[dye2].conc
        xx, yy = np.meshgrid(x,y)
        newx = xx.flatten()
        newy = yy.flatten()
        def myfun(c1,c2):
            fiber = Dyes[dye1].spec[0]
            spec1 = SpecEst(Dyes[dye1].conc,Dyes[dye1].spec,c1)
            spec2 = SpecEst(Dyes[dye2].conc,Dyes[dye2].spec,c2)
            return Merge([c1,c2],[spec1,spec2],fiber,'')
        spec = [myfun(c1,c2) for c1,c2 in zip(newx,newy)]
        return [Spec2LAB(s) for s in spec]
    
    dyes = ['TR101','TY201','TB301']
    
    fig = Figure()     
    canvas = FigureCanvasTkAgg(fig, w)
    canvas.draw()
    ax = fig.add_subplot(111, projection="3d")
    
    
    Lab = []
    
    for i,(d1,d2) in enumerate(permutations(dyes,2)):
        Lab = surface(d1, d2)
        Lab = np.array(Lab)
        ax.plot_trisurf(Lab[:,1], Lab[:,2], Lab[:,0],color=None, linewidth=0.2, antialiased=True)
        #Lab += surface(d1, d2)
    #Lab = np.array(Lab)
    #ax.plot_trisurf(Lab[:,1], Lab[:,2], Lab[:,0],color=None, linewidth=0.2, antialiased=True)
    
    ax.scatter([0],[40],[70],s=300,c='yellow')
    
    ax.set_xlabel("a* Axis")
    ax.set_ylabel("b* Axis")
    ax.set_zlabel("L* Axis")
    ax.set_title("Color Space of Dying")
     
    #toolbar = NavigationToolbar2Tk(canvas, w)
    #toolbar.update()
     
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)   
##   plt.show()

#---------------interface---------------
w = tk.Tk()
w.title("染劑色空間")
w.geometry('800x600')
frame = tk.Frame(w)
frame.pack()

button1 = tk.Button(w, text='draw', fg='red', command= lambda : button_add())
button1.pack(side=tk.LEFT)

button2 = tk.Button(w, text='clean', fg='red', command= lambda : plt.figure.Figure.clear())
button2.pack(side=tk.LEFT)

w.mainloop()