# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:16:29 2022

@author: A90127
"""
import tkinter as tk
from tkinter import ttk
from numpy import array


from app_GUI import GUI
from readme import frame_styles
from cieMath import Spec2RGB, LAB2RGB, Spec2LAB,DE2000
from DyeMerge import SpecEst, Merge, IsFluo, DyeMatch, specTrans

# RGB格式顏色轉換爲16進制顏色格式
def RGB2Hex(RGB):            
    color = '#'
    for i in RGB:
        # 將R、G、B分別轉化爲16進制拼接轉換並大寫  hex() 函數用於將10進制整數轉換成16進制，以字符串形式表示
        color += str(hex(i))[-2:].replace('x', '0').upper()
    return color


class dyeVisionPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.name ='dyeVisionPage'
        
        frame1 = tk.LabelFrame(self,frame_styles,text="光譜輸入")
        frame1.place(relx=0.1,rely=0.02,height=568,width=100)
        frame2 = tk.LabelFrame(self, frame_styles, text="標準樣")
        frame2.place(relx=0.203, rely=0.02, height=280, width=400)
        frame3 = tk.LabelFrame(self, frame_styles, text="對照樣")
        frame3.place(relx=0.203, rely=0.5, height=280, width=400)
        frame4 = tk.LabelFrame(self, frame_styles, text="視覺化")
        frame4.place(relx=0.6, rely=0.02, height=568, width=300)
        frame2_1 = tk.LabelFrame(frame2,frame_styles,text='座標輸入')
        frame2_1.place(relx=0.01,rely=0.00,height=76,width=384)
        frame2_2 = tk.LabelFrame(frame2,frame_styles,text='配方輸入')
        frame2_2.place(relx=0.01,rely=0.31,height=170,width=384)
        
        self.txt1_1 = tk.Text(frame1,width=10,height=36)
        bt1_1 = tk.Button(frame1,text='輸入標準樣',fg='#00F',command=self.std1)
        bt1_2 = tk.Button(frame1,text='輸入對照樣',fg='#00F',command=self.batch1)
        self.txt1_1.pack(fill='both')
        bt1_1.pack(fill='both')
        bt1_2.pack(fill='both')
        
        lb2_1_1 = tk.Label(frame2_1,text='L',width=3)
        lb2_1_1.grid(row=0,column=0,sticky='nsew')
        lb2_1_2 = tk.Label(frame2_1,text='a*',width=3)
        lb2_1_2.grid(row=0,column=2,sticky='nsew')
        lb2_1_3 = tk.Label(frame2_1,text='b*',width=3)
        lb2_1_3.grid(row=0,column=4,sticky='nsew')
        self.et2_1_1 = tk.Entry(frame2_1,width=5,
                                validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.et2_1_1.grid(row=0,column=1,sticky='nsew')
        self.et2_1_2 = tk.Entry(frame2_1,width=5,
                                validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.et2_1_2.grid(row=0,column=3,sticky='nsew')
        self.et2_1_3 = tk.Entry(frame2_1,width=5,
                                validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.et2_1_3.grid(row=0,column=5,sticky='nsew')
        bt2_1_1= tk.Button(frame2_1,text='輸入',fg='#00F',command=self.std2,width=4)
        bt2_1_1.grid(row=1,column=0,sticky='nsew',columnspan=3)
        
        lb2_2_1 = tk.Label(frame2_2,text='胚布材質')
        lb2_2_2 = tk.Label(frame2_2,text='染劑1')
        lb2_2_3 = tk.Label(frame2_2,text='染劑2')
        lb2_2_4 = tk.Label(frame2_2,text='染劑3')
        lb2_2_5 = tk.Label(frame2_2,text='濃度')
        lb2_2_6 = tk.Label(frame2_2,text='濃度')
        lb2_2_7 = tk.Label(frame2_2,text='濃度')
        self.var1 = tk.StringVar()
        self.cb2_2_1 = ttk.Combobox(frame2_2,textvariable=self.var1,
                                   values = ['T','N','D'],
                                   width=6,state="readonly")
        self.cb2_2_1.current(0)
        self.cb2_2_1.bind('<<ComboboxSelected>>', self.dyes_changed1)
        self.var2 = tk.StringVar()
        self.cb2_2_2 = ttk.Combobox(frame2_2,textvariable=self.var2,
                                   values = [''],
                                   width=6,state="readonly")
        self.cb2_2_2.current(0)
        self.var3 = tk.StringVar()
        self.cb2_2_3 = ttk.Combobox(frame2_2,textvariable=self.var3,
                                   values = [''],
                                   width=6,state="readonly")
        self.cb2_2_3.current(0)
        self.var4 = tk.StringVar()
        self.cb2_2_4 = ttk.Combobox(frame2_2,textvariable=self.var4,
                                   values = [''],
                                   width=6,state="readonly")
        self.cb2_2_4.current(0)
        self.et2_2_1 = tk.Entry(frame2_2,width=6,
                                validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.et2_2_2 = tk.Entry(frame2_2,width=6,
                                validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        self.et2_2_3 = tk.Entry(frame2_2,width=6,
                                validate='key',validatecommand=(parent.register(controller.Is_float), '%P'))
        bt2_2_1= tk.Button(frame2_2,text='輸入',fg='#00F',command=self.std3)
        lb2_2_1.grid(row=0,column=0,sticky='ew')
        lb2_2_2.grid(row=1,column=0,sticky='ew')
        lb2_2_3.grid(row=2,column=0,sticky='ew')
        lb2_2_4.grid(row=3,column=0,sticky='ew')
        lb2_2_5.grid(row=1,column=2,sticky='ew')
        lb2_2_6.grid(row=2,column=2,sticky='ew')
        lb2_2_7.grid(row=3,column=2,sticky='ew')
        self.cb2_2_1.grid(row=0,column=1,sticky='ew')        
        self.cb2_2_2.grid(row=1,column=1,sticky='ew')        
        self.cb2_2_3.grid(row=2,column=1,sticky='ew')
        self.cb2_2_4.grid(row=3,column=1,sticky='ew')
        self.et2_2_1.grid(row=1,column=3)
        self.et2_2_2.grid(row=2,column=3)
        self.et2_2_3.grid(row=3,column=3)
        bt2_2_1.grid(row=4,column=0,sticky='nsew',columnspan=2)
    
        lb3_1 = tk.Label(frame3,text='胚布材質')
        lb3_2 = tk.Label(frame3,text='染劑1')
        lb3_3 = tk.Label(frame3,text='染劑2')
        lb3_4 = tk.Label(frame3,text='染劑3')
        lb3_5 = tk.Label(frame3,text='DL',width=3,fg='#F00')        
        lb3_6 = tk.Label(frame3,text='Da*',width=3,fg='#F00')        
        lb3_7 = tk.Label(frame3,text='Db*',width=3,fg='#F00')
        lb3_8 = tk.Label(frame3,text='DE',width=3,fg='#F00')
        self.lb3_9 = tk.Label(frame3,width=8,relief='ridge',fg='#080')
        self.lb3_10 = tk.Label(frame3,width=8,relief='ridge',fg='#080')
        self.lb3_11 = tk.Label(frame3,width=8,relief='ridge',fg='#080')
        self.lb3_12 = tk.Label(frame3,width=8,relief='ridge',fg='#080')
        self.var5 = tk.StringVar()
        self.cb3_1 = ttk.Combobox(frame3,textvariable=self.var5,
                                   values = ['T','N','D'],
                                   width=6,state="readonly")
        self.cb3_1.current(0)
        self.cb3_1.bind('<<ComboboxSelected>>', self.dyes_changed2)
        self.var6 = tk.StringVar()
        self.cb3_2 = ttk.Combobox(frame3,textvariable=self.var6,
                                   values = [''],
                                   width=6,state="readonly")
        self.cb3_2.current(0)
        self.var7 = tk.StringVar()
        self.cb3_3 = ttk.Combobox(frame3,textvariable=self.var7,
                                   values = [''],
                                   width=6,state="readonly")
        self.cb3_3.current(0)
        self.var8 = tk.StringVar()
        self.cb3_4 = ttk.Combobox(frame3,textvariable=self.var8,
                                   values = [''],
                                   width=6,state="readonly")
        self.cb3_4.current(0)
        self.sc3_1 = tk.Scale(frame3,from_= 0,to=1,resolution=0.0001,command=self.batch4,orient='horizontal')
        self.sc3_2 = tk.Scale(frame3,from_= 0,to=1,resolution=0.0001,command=self.batch4,orient='horizontal')
        self.sc3_3 = tk.Scale(frame3,from_= 0,to=1,resolution=0.0001,command=self.batch4,orient='horizontal')
        bt3_1 = tk.Button(frame3,text='原胚打色',fg='#00F',command=self.batch2)
        bt3_2 = tk.Button(frame3,text='色胚打色',fg='#00F',command=self.batch3)
        lb3_1.grid(row=1,column=0,sticky='nsew')
        lb3_2.grid(row=2,column=0,sticky='nsew')
        lb3_3.grid(row=3,column=0,sticky='nsew')
        lb3_4.grid(row=4,column=0,sticky='nsew')
        bt3_1.grid(row=5,column=0,columnspan=2,sticky='nsew')
        bt3_2.grid(row=6,column=0,columnspan=2,sticky='nsew')
        lb3_5.grid(row=0,column=0,sticky='nsew')
        lb3_6.grid(row=0,column=2,sticky='nsew')
        lb3_7.grid(row=0,column=4,sticky='nsew')
        lb3_8.grid(row=0,column=6,sticky='nsew')
        self.lb3_9.grid(row=0,column=1,sticky='nsew')
        self.lb3_10.grid(row=0,column=3,sticky='nsew')
        self.lb3_11.grid(row=0,column=5,sticky='nsew')
        self.lb3_12.grid(row=0,column=7,sticky='nsew')
        self.cb3_1.grid(row=1,column=1,sticky='nsew')
        self.cb3_2.grid(row=2,column=1,sticky='nsew')
        self.cb3_3.grid(row=3,column=1,sticky='nsew')
        self.cb3_4.grid(row=4,column=1,sticky='nsew')
        self.sc3_1.grid(row=2,column=2,columnspan=6,sticky='nsew')
        self.sc3_2.grid(row=3,column=2,columnspan=6,sticky='nsew')
        self.sc3_3.grid(row=4,column=2,columnspan=6,sticky='nsew')
    
        self.lb4_1 = tk.Label(frame4,bg='#FFF')
        self.lb4_2 = tk.Label(frame4,bg='#000')
        self.lb4_1.grid(row=0,column=0,ipadx=142,ipady=126,sticky='nesw')
        self.lb4_2.grid(row=1,column=0,ipadx=142,ipady=125,sticky='nesw')
        
        
    #標準樣光譜輸入    
    def std1(self):
        self.spec = self.txt1_1.get('1.0','end').split('\n')
        self.stdspec = array([float(i) for i in self.spec if i])
        self.lb4_1.config(bg=RGB2Hex(Spec2RGB(self.stdspec)))
        self.stdlab = Spec2LAB(self.stdspec)
        self.et2_1_1.delete(0,'end')
        self.et2_1_1.insert(0,round(self.stdlab[0],2))
        self.et2_1_2.delete(0,'end')
        self.et2_1_2.insert(0,round(self.stdlab[1],2))
        self.et2_1_3.delete(0,'end')
        self.et2_1_3.insert(0,round(self.stdlab[2],2))
    #標準樣Lab輸入    
    def std2(self):
        self.stdlab = [self.et2_1_1.get(),self.et2_1_2.get(),self.et2_1_3.get()]
        self.stdlab = array([float(i) for i in self.stdlab])
        self.lb4_1.config(bg=RGB2Hex(LAB2RGB(self.stdlab)))
    #標準樣配方輸入
    def std3(self):
        dyes = [self.var2.get(),self.var3.get(),self.var4.get()]
        dyes = [d for d in dyes if d]
        concs = [self.et2_2_1.get(), self.et2_2_2.get(),self.et2_2_3.get()]
        concs = [float(i) for i in concs if i]
        fiber = self.Dyes[dyes[0]].spec[0]
        fl = IsFluo(dyes)
        if fl:
            C = sum(concs)
            specs = [SpecEst(self.Dyes[d].conc,self.Dyes[d].spec,C,IsFluo([d])) for d in dyes]
            self.stdspec = Merge(concs,specs,fiber,'nonequi',fl)
        else:
            specs = [SpecEst(self.Dyes[d].conc,self.Dyes[d].spec,c,IsFluo([d])) for c,d in zip(concs,dyes)]
            self.stdspec = Merge(concs,specs,fiber,'KSadd',fl)
        self.stdlab = Spec2LAB(self.stdspec)
        self.et2_1_1.delete(0,'end')
        self.et2_1_1.insert(0,round(self.stdlab[0],2))
        self.et2_1_2.delete(0,'end')
        self.et2_1_2.insert(0,round(self.stdlab[1],2))
        self.et2_1_3.delete(0,'end')
        self.et2_1_3.insert(0,round(self.stdlab[2],2))
        self.lb4_1.config(bg=RGB2Hex(LAB2RGB(self.stdlab)))
        
        
    #對照樣光譜輸入    
    def batch1(self):
        self.batchspec = self.txt1_1.get('1.0','end').split('\n')
        self.batchspec = array([float(i) for i in self.batchspec if i])
        self.batchlab = Spec2LAB(self.batchspec)
        self.lb4_2.config(bg=RGB2Hex(Spec2RGB(self.batchspec)))
        
    #原胚打色變數設定    
    def batch2(self):
        dyes = [self.var6.get(),self.var7.get(),self.var8.get()]
        scales = [self.sc3_1,self.sc3_2,self.sc3_3]
        for d,sc in zip(dyes,scales):
            if d:
                self.fibspec = self.Dyes[d].spec[0]
                self.batchspec = self.Dyes[d].spec[0]
                self.lb4_2.config(bg=RGB2Hex(Spec2RGB(self.batchspec)))
                sc.config(from_=0,to=self.Dyes[d].conc[-1],
                          resolution=0.0001)
                sc.set(0) 
        self.batchlab = Spec2LAB(self.batchspec)
        self.lb4_2.config(bg=RGB2Hex(LAB2RGB(self.batchlab)))
        self.lb3_9.config(text=round(self.batchlab[0]-self.stdlab[0],2))
        self.lb3_10.config(text=round(self.batchlab[1]-self.stdlab[1],2))
        self.lb3_11.config(text=round(self.batchlab[2]-self.stdlab[2],2))
        self.lb3_12.config(text=round(DE2000(self.batchlab,self.stdlab),2))
    #色胚打色變數設定
    def batch3(self):
        dyes = [self.var6.get(),self.var7.get(),self.var8.get()]
        self.fibspec = self.batchspec
        scales = [self.sc3_1,self.sc3_2,self.sc3_3]
        for d,sc in zip(dyes,scales):
            if d:
                sc.config(from_=0,to=self.Dyes[d].conc[-1],
                          resolution=0.0001)
                sc.set(0)
        self.batchlab = Spec2LAB(self.fibspec)
        self.lb3_9.config(text=round(self.batchlab[0]-self.stdlab[0],2))
        self.lb3_10.config(text=round(self.batchlab[1]-self.stdlab[1],2))
        self.lb3_11.config(text=round(self.batchlab[2]-self.stdlab[2],2))
        self.lb3_12.config(text=round(DE2000(self.batchlab,self.stdlab),2))
                                  
    #滾軸輸入
    def batch4(self,*arg):
        concs = [self.sc3_1.get(), self.sc3_2.get(),self.sc3_3.get()]
        dyes = [self.var6.get(),self.var7.get(),self.var8.get()]
        concs = [c for c,d in zip(concs,dyes) if d]
        dyes = [d for d in dyes if d]
        if IsFluo(dyes):
            C = sum(concs)
            specs = [SpecEst(self.Dyes[d].conc,
                             specTrans(self.Dyes[d].spec,self.fibspec,IsFluo([d])),
                             C,IsFluo([d])) for d in dyes]
            self.batchspec = Merge(concs,specs,self.fibspec,'nonequi',True)
        else:
            specs = [SpecEst(self.Dyes[d].conc,
                             specTrans(self.Dyes[d].spec,self.fibspec,IsFluo([d])),
                             c,IsFluo([d])) for c,d in zip(concs,dyes)]
            self.batchspec = Merge(concs,specs,self.fibspec,'KSadd',False)
        self.lb4_2.config(bg=RGB2Hex(Spec2RGB(self.batchspec)))
        self.batchlab = Spec2LAB(self.batchspec)
        self.lb3_9.config(text=round(self.batchlab[0]-self.stdlab[0],2))
        self.lb3_10.config(text=round(self.batchlab[1]-self.stdlab[1],2))
        self.lb3_11.config(text=round(self.batchlab[2]-self.stdlab[2],2))
        self.lb3_12.config(text=round(DE2000(self.batchlab,self.stdlab),2))
        
    def dyes_changed1(self,*arg):
        m = self.var1.get()
        ls = sorted(['']+[d for d in self.Dyes.keys() 
                           if self.Dyes[d].material==m])
        self.cb2_2_2['values'] = ls
        self.cb2_2_3['values'] = ls
        self.cb2_2_4['values'] = ls
        
    def dyes_changed2(self,*arg):
        m = self.var5.get()
        ls = sorted(['']+[d for d in self.Dyes.keys() 
                           if self.Dyes[d].material==m])
        self.cb3_2['values'] = ls
        self.cb3_3['values'] = ls
        self.cb3_4['values'] = ls