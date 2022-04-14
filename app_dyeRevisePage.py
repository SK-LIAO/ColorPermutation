# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:14:54 2022

@author: A90127
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from app_GUI import GUI
from readme import frame_styles
from numpy import array
from DyeMerge import ConcCentroid


class dyeRevisePage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.name ='dyeRevisePage'
        frame1 = tk.LabelFrame(self, frame_styles, text="參數設定")
        frame1.place(relx=0.1, rely=0.02, height=550, width=232)
        frame2 = tk.LabelFrame(self, frame_styles, text="色差空間")
        frame2.place(relx=0.33, rely=0.02, height=550, width=570)
        
        lb1 = tk.Label(frame1,text='濃度1',fg='#F00',width=8)
        lb2 = tk.Label(frame1,text='濃度2',fg='#F00',width=8)
        lb3 = tk.Label(frame1,text='濃度3',fg='#F00',width=8)
        lb4 = tk.Label(frame1,text='DL',fg='#F00')
        lb5 = tk.Label(frame1,text='Da*',fg='#F00')
        lb6 = tk.Label(frame1,text='Db*',fg='#F00')
        lb7 = tk.Label(frame1,text='配方1',fg='#00F')
        lb8 = tk.Label(frame1,text='配方2',fg='#00F')
        lb9 = tk.Label(frame1,text='配方3',fg='#00F')
        lb10 = tk.Label(frame1,text='配方4',fg='#00F')
        lb11 = tk.Label(frame1,text='配方1',fg='#00F')
        lb12 = tk.Label(frame1,text='配方2',fg='#00F')
        lb13 = tk.Label(frame1,text='配方3',fg='#00F')
        lb14 = tk.Label(frame1,text='配方4',fg='#00F')
        lb15 = tk.Label(frame1,text='染劑',fg='#F00')
        lb16 = tk.Label(frame1,text='色差',fg='#F00')
        lb1.grid(row=0,column=1,sticky='nsew')
        lb2.grid(row=0,column=2,sticky='nsew')
        lb3.grid(row=0,column=3,sticky='nsew')
        lb4.grid(row=5,column=1,sticky='nsew')
        lb5.grid(row=5,column=2,sticky='nsew')
        lb6.grid(row=5,column=3,sticky='nsew')
        lb7.grid(row=1,column=0,sticky='nsew')
        lb8.grid(row=2,column=0,sticky='nsew')
        lb9.grid(row=3,column=0,sticky='nsew')
        lb10.grid(row=4,column=0,sticky='nsew')
        lb11.grid(row=6,column=0,sticky='nsew')
        lb12.grid(row=7,column=0,sticky='nsew')
        lb13.grid(row=8,column=0,sticky='nsew')
        lb14.grid(row=9,column=0,sticky='nsew')
        lb15.grid(row=0,column=0,sticky='nsew')
        lb16.grid(row=5,column=0,sticky='nsew')
        self.et = {}
        for i in [1,2,3,4,6,7,8,9]:
            for j in [1,2,3]:
                self.et[(i,j)] = tk.Entry(frame1,width=7,
                                          validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
                self.et[(i,j)].grid(row=i,column=j,sticky='nsew')
        bt1 = tk.Button(frame1,text='推薦配方濃度',command=self.analysis,fg='#00F')
        lb17 = tk.Label(frame1,text='配方',fg='#00F')
        self.lb18 = tk.Label(frame1,fg='#080',relief='ridge')
        self.lb19 = tk.Label(frame1,fg='#080',relief='ridge')
        self.lb20 = tk.Label(frame1,fg='#080',relief='ridge')
        bt1.grid(row=11,column=0,sticky='nsew',columnspan=4)
        lb17.grid(row=12,column=0,sticky='nsew')
        self.lb18.grid(row=12,column=1,sticky='nsew')
        self.lb19.grid(row=12,column=2,sticky='nsew')
        self.lb20.grid(row=12,column=3,sticky='nsew')
        
        fig = Figure()         
        self.canvas = FigureCanvasTkAgg(fig,frame2)
        self.canvas.draw()
        self.ax = fig.add_subplot(111, projection="3d")
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def analysis(self):
        mat1 = array([ [float(self.et[(i,j)].get()) for j in [1,2,3]] for i in [1,2,3,4] ])
        mat2 = array([ [float(self.et[(i,j)].get()) for j in [1,2,3]] for i in [6,7,8,9] ])
        center = array([0,0,0])
        conc = ConcCentroid(mat1,mat2)
        self.lb18.config(text=round(conc[0],4))
        self.lb19.config(text=round(conc[1],4))
        self.lb20.config(text=round(conc[2],4))
        self.ax.clear()
        curve1 = array([mat2[0],center,mat2[1],center,mat2[2],center,mat2[3]])
        curve2 = array([mat2[0],mat2[1],mat2[2],mat2[0],mat2[3],mat2[1],mat2[3],mat2[2]])
        self.ax.plot(curve1[:,1],curve1[:,2],curve1[:,0])
        self.ax.plot(curve2[:,1],curve2[:,2],curve2[:,0])
        self.ax.scatter([0],[0],[0],s=120,c='#F00',marker='*')
        for x,y,z,label in zip(mat2[:,1],mat2[:,2],mat2[:,0],['Recipe 1','Recipe 2','Recipe 3','Recipe 4']):
            self.ax.text(x,y,z,label)
        self.ax.set_xlabel("Da* ",c='#F00',fontsize=20)
        self.ax.set_ylabel("Db*",c='#F00',fontsize=20)
        self.ax.set_zlabel("DL",c='#F00',fontsize=20)
        self.ax.set_title("Delta La*b* Space of Dying")
        self.canvas.draw()
        