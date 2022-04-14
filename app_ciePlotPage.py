# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:10:01 2022

@author: A90127
"""
import tkinter as tk
from tkinter import ttk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from itertools import permutations

from app_GUI import GUI
from readme import frame_styles
from DyeMerge import SpecEst, Merge, IsFluo, DyeMatch
from cieMath import Spec2LAB

class ciePlotPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.name = 'ciePlotPage'
        frame1 = tk.LabelFrame(self, frame_styles, text="CIE Space")
        frame1.place(relx=0.33, rely=0.02, height=550, width=570)
        frame2 = tk.LabelFrame(self, frame_styles, text="染劑選擇")
        frame2.place(relx=0.1, rely=0.02, height=550, width=232)
        
        Label1 = tk.Label(frame2,text='胚布材質',width=10)
        self.var1 = tk.StringVar()
        self.Combobox1_1 = ttk.Combobox(frame2,textvariable=self.var1,
                                   values = ['T','N','D'],width=8,state="readonly")
        self.Combobox1_1.current(0)
        self.Combobox1_1.bind('<<ComboboxSelected>>', self.dyes_changed)
        Label2 = tk.Label(frame2,text='染劑1')
        self.var2 = tk.StringVar()
        self.Combobox2_1 = ttk.Combobox(frame2,textvariable=self.var2,
                                   values = [''],width=8,state="readonly")
        self.Combobox2_1.current(0)
        Label3 = tk.Label(frame2,text='染劑2')
        self.var3 = tk.StringVar()
        self.Combobox3_1 = ttk.Combobox(frame2,textvariable=self.var3,
                                   values = [''],width=8,state="readonly")
        self.Combobox3_1.current(0)
        Label4 = tk.Label(frame2,text='染劑3')
        self.var4 = tk.StringVar()
        self.Combobox4_1 = ttk.Combobox(frame2,textvariable=self.var4,
                                   values = [''],width=8,state="readonly")
        self.Combobox4_1.current(0)
        fig = Figure()         
        self.canvas = FigureCanvasTkAgg(fig,frame1)
        self.canvas.draw()
        self.ax = fig.add_subplot(111, projection="3d")
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        Button1 = tk.Button(frame2,fg='#00F',text='色域空間繪圖',command=self.plotArea)
        Button2 = tk.Button(frame2,fg='#00F',text='染劑曲線繪圖',command=self.plotCurve)
        Label5 = tk.Label(frame2,text='標準樣L')
        Label6 = tk.Label(frame2,text='標準樣a*')
        Label7 = tk.Label(frame2,text='標準樣b*')
        self.Entry1 = tk.Entry(frame2,width=8,
                               validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.Entry2 = tk.Entry(frame2,width=8,
                               validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.Entry3 = tk.Entry(frame2,width=8,
                               validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        Button3 = tk.Button(frame2,fg='#00F',text='匯入標準樣座標',command=self.plotStd)
        Button4 = tk.Button(frame2,fg='#00F',text='找配方',command=self.match)
        Label8 = tk.Label(frame2,text='染劑1濃度',fg='#F00')
        Label9 = tk.Label(frame2,text='染劑2濃度',fg='#F00')
        Label10 = tk.Label(frame2,text='染劑3濃度',fg='#F00')
        Label11 = tk.Label(frame2,text='色差',fg='#F00')
        self.Label12 = tk.Label(frame2,relief='ridge',fg='#080')
        self.Label13 = tk.Label(frame2,relief='ridge',fg='#080')
        self.Label14 = tk.Label(frame2,relief='ridge',fg='#080')
        self.Label15 = tk.Label(frame2,relief='ridge',fg='#080')
        Label1.grid(row=1,column=0,sticky='nsew')
        Label2.grid(row=2,column=0,sticky='nsew')
        Label3.grid(row=3,column=0,sticky='nsew')
        Label4.grid(row=4,column=0,sticky='nsew')
        self.Combobox1_1.grid(row=1,column=1,sticky='nsew')
        self.Combobox2_1.grid(row=2,column=1,sticky='nsew')
        self.Combobox3_1.grid(row=3,column=1,sticky='nsew')
        self.Combobox4_1.grid(row=4,column=1,sticky='nsew')
        Button1.grid(row=5,column=0,sticky='nsew',columnspan=2)
        Button2.grid(row=6,column=0,sticky='nsew',columnspan=2)
        Label5.grid(row=7,column=0,sticky='nsew')
        Label6.grid(row=8,column=0,sticky='nsew')
        Label7.grid(row=9,column=0,sticky='nsew')
        self.Entry1.grid(row=7,column=1,sticky='nsew')
        self.Entry2.grid(row=8,column=1,sticky='nsew')
        self.Entry3.grid(row=9,column=1,sticky='nsew')
        Button3.grid(row=10,column=0,sticky='nsew',columnspan=2)
        Button4.grid(row=11,column=0,sticky='nsew',columnspan=2)
        Label8.grid(row=12,column=0,sticky='nsew')
        Label9.grid(row=13,column=0,sticky='nsew')
        Label10.grid(row=14,column=0,sticky='nsew')
        Label11.grid(row=15,column=0,sticky='nsew')
        self.Label12.grid(row=12,column=1,sticky='nsew')
        self.Label13.grid(row=13,column=1,sticky='nsew')
        self.Label14.grid(row=14,column=1,sticky='nsew')
        self.Label15.grid(row=15,column=1,sticky='nsew')
        
    def match(self):
        dyes = [self.var2.get(),self.var3.get(),self.var4.get()]
        lab = [self.Entry1.get(),self.Entry2.get(),self.Entry3.get()]
        lab = np.array([float(i) for i in lab])
        concls = [self.Dyes[d].conc for d in dyes if d]
        specls = [self.Dyes[d].spec for d in dyes if d]
        flls = [IsFluo([d]) for d in dyes if d]
        cAprox, deltaE, labAprox = DyeMatch(lab,concls,specls,flls)
        Labels = [self.Label12,self.Label13,self.Label14]
        i0=0
        for i,(d,L) in enumerate(zip(dyes,Labels)):
            L.config(text='')
            if d:
                L.config(text=round(cAprox[i0],4))
                i0 += 1
        self.Label15.config(text=round(deltaE,2))
            
        
    def plotStd(self):
        x = float(self.Entry2.get())
        y = float(self.Entry3.get())
        z = float(self.Entry1.get())
        self.ax.scatter([x],[y],[z],s=120,c='#F00',marker='*')
        self.canvas.draw()
                
    def plotCurve(self):
        self.ax.clear()
        dyes = [self.var2.get(),self.var3.get(),self.var4.get()]
        dyes = [d for d in dyes if d]
        name = ''
        for d in dyes:
            labs = np.array([Spec2LAB(spec) for spec in self.Dyes[d].spec])
            if d != name:
                ind = len(labs)//2+1
                self.ax.text(labs[ind,1],labs[ind,2],labs[ind,0],d)
                name = d
            self.ax.plot(labs[:,1],labs[:,2],labs[:,0])
            
        self.ax.set_xlabel("a* Axis")
        self.ax.set_ylabel("b* Axis")
        self.ax.set_zlabel("L* Axis")
        self.ax.set_title("Color Space of Dying")
        self.canvas.draw()
            
        
    def plotArea(self):
        self.ax.clear()
        dyes = [self.var2.get(),self.var3.get(),self.var4.get()]
        dyes = [d for d in dyes if d]
        fl = IsFluo(dyes)
        def surface(dye1,dye2):
            x = self.Dyes[dye1].conc
            y = self.Dyes[dye2].conc
            xx, yy = np.meshgrid(x,y)
            newx = xx.flatten()
            newy = yy.flatten()
            def myfun(c1,c2):
                fiber = self.Dyes[dye1].spec[0]
                if fl:
                    c = c1+c2
                    spec1 = SpecEst(self.Dyes[dye1].conc,self.Dyes[dye1].spec,c,IsFluo([dye1]))
                    spec2 = SpecEst(self.Dyes[dye2].conc,self.Dyes[dye2].spec,c,IsFluo([dye2]))
                    return Merge([c1,c2],[spec1,spec2],fiber,'nonequi',fl)
                else:
                    spec1 = SpecEst(self.Dyes[dye1].conc,self.Dyes[dye1].spec,c1,IsFluo([dye1]))
                    spec2 = SpecEst(self.Dyes[dye2].conc,self.Dyes[dye2].spec,c2,IsFluo([dye2]))
                    return Merge([c1,c2],[spec1,spec2],fiber,'KSadd',fl)
            spec = [myfun(c1,c2) for c1,c2 in zip(newx,newy)]
            return [Spec2LAB(s) for s in spec]
        
        Lab = []
        for i,(d1,d2) in enumerate(permutations(dyes,2)):
            Lab = surface(d1, d2)
            Lab = np.array(Lab)
            self.ax.plot_trisurf(Lab[:,1], Lab[:,2], Lab[:,0],color=None, linewidth=0.2, antialiased=True)
            #Lab += surface(d1, d2)
        #Lab = np.array(Lab)
        #ax.plot_trisurf(Lab[:,1], Lab[:,2], Lab[:,0],color=None, linewidth=0.2, antialiased=True)
        
        self.ax.set_xlabel("a* Axis")
        self.ax.set_ylabel("b* Axis")
        self.ax.set_zlabel("L* Axis")
        self.ax.set_title("Color Space of Dying")
        self.canvas.draw()
        
    def dyes_changed(self,*arg):
        m = self.var1.get()
        ls = sorted(['']+[d for d in self.Dyes.keys() 
                           if self.Dyes[d].material==m])
        self.Combobox2_1['values'] = ls
        self.Combobox3_1['values'] = ls
        self.Combobox4_1['values'] = ls