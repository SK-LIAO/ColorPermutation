# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 08:22:58 2022

@author: A90127
"""
import tkinter as tk

from numpy import array
from tkinter import ttk
from pyperclip import copy
from operator import xor

from VerticalScrolledFrame import VerticalScrolledFrame 
from app_GUI import GUI
from readme import frame_styles
from dataBuild import app_meargeSearch, app_recipeDict
from DyeMerge import ContactDE, app_colorVisual,IsFluo,RGB2Hex
from Permutation import app_colorPermutation
from cieMath import LAB2RGB


class MainPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        
        self.controller = controller
        frame1 = tk.LabelFrame(self, frame_styles, text="查詢可排染工卡")
        frame1.place(relx=0.1, rely=0.02, width=202, height=178)  
        frame2 = tk.LabelFrame(self,frame_styles,text='接缸色差計算機')
        frame2.place(relx=0.1, rely=0.33, width=202, height=178)
        frame4 = tk.LabelFrame(self, frame_styles, text="查詢併染工卡")
        frame4.place(relx=0.1, rely=0.64, width=202, height=178)
        
        lb1_1 = tk.Label(frame1,text='缸量(起)')
        lb1_2 = tk.Label(frame1,text='缸量(迄)')
        #判斷是否為3位數整數用
        def numValidate(P):
            if len(P)<=3:
                return str.isdigit(P) or P==''
            else:
                return False
        ent1_1 = tk.Entry(frame1,width=5,justify='r',
                         validate='key', 
                         validatecommand=(parent.register(numValidate), '%P'))
        ent1_2 = tk.Entry(frame1,width=5,justify='r',
                         validate='key', 
                         validatecommand=(parent.register(numValidate), '%P'))
        bt1_1 = tk.Button(frame1,text='查詢',fg='#00E',
                          command=lambda :tvpt())
        '''染色排序 待完成'''
        bt1_2 = tk.Button(frame1,text='排序',fg='#00E',
                          command=lambda :sortColor())
        lb1_1.grid(row=0,column=0,sticky='ew')
        lb1_2.grid(row=1,column=0,sticky='ew')
        ent1_1.grid(row=0,column=1,sticky='ew')
        ent1_2.grid(row=1,column=1,sticky='ew')
        bt1_1.grid(row=2,column=0,sticky='ew')
        bt1_2.grid(row=3,column=0,sticky='ew')
        
        lb2_1 = tk.Label(frame2,text ='前工卡')
        lb2_2 = tk.Label(frame2,text ='後工卡')
        #判斷使否為工卡形式的函數
        def Evalidate(P):
            #print(P)
            if len(P)==0:
                return True
            elif len(P)==1:
                return P=='E'
            elif len(P)<=10:
                return str.isdigit(P[1:])
            elif len(P)<=13:
                return True
            else:
                return False
        var1 = tk.StringVar()
        #限制輸入形式滿足工卡形式
        ent2_1 = tk.Entry(frame2,textvariable=var1,width=18,
                         validate='key', 
                         validatecommand=(parent.register(Evalidate), '%P'))        
        var2 = tk.StringVar()
        #限制輸入形式滿足工卡形式
        ent2_2 = tk.Entry(frame2,textvariable=var2,width=18,
                         validate='key', 
                         validatecommand=(parent.register(Evalidate), '%P'))
        bt2_1 = tk.Button(frame2,text='接色DE',fg='#00E',
                          command=lambda :deltaE())
        var3 = tk.DoubleVar()
        var3.set(0)
        lb2_3 = tk.Label(frame2,textvariable=var3,fg='blue',width=4)
        lb2_1.grid(row=0,column=0,sticky='ew')
        lb2_2.grid(row=1,column=0,sticky='ew')
        lb2_3.grid(row=2,column=1,sticky='w')
        ent2_1.grid(row=0,column=1,sticky='ew')
        ent2_2.grid(row=1,column=1,sticky='ew')
        bt2_1.grid(row=2,column=0,sticky='ew')
        
        lb4_1 = tk.Label(frame4,text ='工卡號')
        var4 = tk.StringVar()
        #限制輸入形式滿足工卡形式
        ent4_1 = tk.Entry(frame4,textvariable=var4,width=18,
                         validate='key', 
                         validatecommand=(parent.register(Evalidate), '%P'))
        bt4_1 = tk.Button(frame4,text='查詢',fg='#00E',
                          command=lambda:CheckMerge(self,controller))
        lb4_1.grid(row=0,column=0,sticky='ew')
        ent4_1.grid(row=0,column=1,sticky='ew')
        bt4_1.grid(row=1,column=0,sticky='ew')
        
        
        frame3 = tk.LabelFrame(self, frame_styles, text="可染色工卡")
        frame3.place(relx=0.3, rely=0.02, height=550, width=600)
        head = ('工卡號','指染單號','開卡量','併染量','顏色','配方')
        self.tv = ttk.Treeview(frame3,
                          columns=head,
                          show='headings',
                          selectmode='extended')
        widths = [100,80,50,50,250,800]
        anchors = ['w','w','c','c','w','w',]
        # define headings, column
        for ls,w,a in zip(head,widths,anchors):
            self.tv.heading(ls, text=ls)
            self.tv.column(ls,width=w,anchor=a)
        
        
        #設定y軸滑桿
        ytreescroll = tk.Scrollbar(frame3,
                                   command=self.tv.yview)
        self.tv.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")
        self.tv.place(relheight=0.995, relwidth=0.995)
        #設定x軸滑桿
        xtreescroll = tk.Scrollbar(frame3,
                                   command=self.tv.xview,
                                   orient='horizontal')
        self.tv.configure(xscrollcommand=xtreescroll.set)
        xtreescroll.pack(side="bottom", fill="x")
        #雙擊選單事件: 複製工卡號/複製指染單號
        def copyEKA(event):
            menu = tk.Menu(parent,tearoff=0)
            def copyinE():
                for item  in self.tv.selection():
                    item_text = self.tv.item(item,"values")
                card = item_text[0]
                copy(card)
            def copyinKA():
                for item  in self.tv.selection():
                    item_text = self.tv.item(item,"values")
                card = item_text[1]
                copy(card)
            def colorVisual():
                self.eventx = event.x_root
                self.eventy = event.y_root
                CheckColor(self,controller)
            menu.add_command(label='複製工卡號',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製指染單號',command=copyinKA)
            '''跳出工卡顏色視窗'''
            menu.add_command(label='查看顏色',command=colorVisual)
            menu.post(event.x_root, event.y_root)
        def mergeCheck(event):
            CheckMerge(self,controller)
        self.tv.bind('<Double-1>', mergeCheck)
        self.tv.bind('<Button-3>', copyEKA)
        self.tv.place(relheight=0.995, relwidth=0.995)
        
        def tvpt():
            #初始化
            Refresh_data()
            #缸量範圍值
            m, M = int(ent1_1.get()), int(ent1_2.get())
            self.search = app_meargeSearch(controller.waitDye,controller.recipeE,controller.mergeE,m,M)
            for row in self.search:
                s = ' '.join([i.__str__() for i in row[-1]])
                row[-1]=s
                self.tv.insert('', 'end', values=tuple(row))
            self.tv.insert('', 'end', values=[''])
            #拉出有搜尋到工卡的配方data
            recipeData = array([d for d in controller.recipeE if d[0] in array(self.search)[:,0]])
            #建立配方字典
            self.recipeDict = app_recipeDict(recipeData)
            
        def sortColor():
            ColorPermutation(self,controller)
            
        
        def deltaE():
            E1,E2 = ent2_1.get(), ent2_2.get()
            #警告是否出現 螢光接非螢光 或 非螢光接螢光。
            self.warning(E1,E2)
            DE = ContactDE(E1,E2,self.recipeDict,controller.Dyes)
            var3.set(round(DE,2))
        
        def Refresh_data():
            # Deletes the data in the current treeview and reinserts it.
            self.tv.delete(*(self.tv).get_children())
            
    '''計算機警告螢光劑接色'''
    def warning(self,E1,E2):
        T1, T2 = IsFluo(self.recipeDict[E1].dyes), IsFluo(self.recipeDict[E2].dyes)
        a = {}
        a[E1] = '螢光色' if T1 else '非螢光色'
        a[E2] ='螢光色' if T2 else '非螢光色'
        if xor(T1,T2):
            tk.messagebox.showinfo(title='注意', message='此為{}工卡接到{}工卡'.format(a[E1],a[E2]))

#挑出該工卡的顏色視窗
class CheckColor(tk.Toplevel):
    def __init__(self, parent,controller):
        tk.Toplevel.__init__(self, parent, bg="#FFF")
        
        #找出點選的工卡號
        for item in parent.tv.selection():
            item_text = parent.tv.item(item,"values")
        card = item_text[0]
        self.title(card)
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("300x100+"+parent.eventx.__str__()+"+"+parent.eventy.__str__()) #fixes the applications size
        self.iconbitmap('LC.ico')
        
        #回傳材質對應顏色的RGB字典
        colorDict = app_colorVisual(card,parent.recipeDict,controller.Dyes)
        labelDict ={}
        for key in colorDict.keys():
            labelDict[key] = tk.Label(self,text=key,font=("Helvetica", 20),bg=colorDict[key])
            for i in [1,3,5]:
                if colorDict[key][i:i+2]>'60':
                    break
            else:
                labelDict[key].config(fg='#FFF')
            labelDict[key].pack(fill='both',expand=True,side='left')
                
#挑出併染工卡視窗
class CheckMerge(tk.Toplevel):
    def __init__(self, parent,controller):
        tk.Toplevel.__init__(self, parent, bg="#BEB2A7")
        
        self.title('併染工卡')
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("500x300+100+20") #fixes the applications size
        self.iconbitmap('LC.ico')
        for item in parent.tv.selection():
            item_text = parent.tv.item(item,"values")
        frame = tk.LabelFrame(self,frame_styles,text=item_text[0]+"併染工卡")
        frame.place(relx=0.02,rely=0.02,height=290,width=490)
        
        head = ['工卡號','染單單號','表頭狀態','開卡量']
        tv = ttk.Treeview(frame,
                          selectmode='browse',
                          columns = head,
                          show = 'headings')
        widths = [100,100,100,100]
        anchors = ['w','w','c','c',]
        # define headings, column
        for ls,w,a in zip(head,widths,anchors):
            tv.heading(ls, text=ls)
            tv.column(ls,width=w,anchor=a)
        
        ytreescroll = tk.Scrollbar(frame)
        ytreescroll.configure(command=tv.yview)
        tv.configure(yscrollcommand=ytreescroll.set)
        ytreescroll.pack(side="right", fill="y")

        maincard = item_text[0]
        try:
            s = list(controller.mergeE[maincard]) 
        except:
            s = []    
        mergecards = [maincard] + s  
        mat = [d for d in controller.waitDye if d[0] in mergecards]
        for row in mat:
            tv.insert('', 'end', values=list(row[:4]))
        
        def copyEKA(event):
            menu = tk.Menu(parent,tearoff=0)
            def copyinE():
                for item  in tv.selection():
                    item_text = tv.item(item,"values")
                card = item_text[0]
                copy(card)    
            def copyinKA():
                for item  in tv.selection():
                    item_text = tv.item(item,"values")
                card = item_text[1]
                copy(card)
            menu.add_command(label='複製工卡號',command=copyinE) #點擊後複製工卡號
            menu.add_command(label='複製染單號',command=copyinKA)#點擊後複製工卡號 
            menu.post(event.x_root, event.y_root)
        tv.bind('<Button-3>', copyEKA) #雙擊出現複製選單
        tv.place(relheight=0.995, relwidth=0.995)

#跳出工卡排序視窗       
class ColorPermutation(tk.Toplevel):
    def __init__(self, parent,controller):
        tk.Toplevel.__init__(self, parent, bg="#FFF")
        
        self.title('接色排序結果')
        self.resizable(0, 1) #prevents the app from being resized
        self.geometry("1000x300+50+10") #fixes the applications size
        self.iconbitmap('LC.ico')
        
        #抓取要排序的工卡號
        Ecards = [parent.tv.item(item)['values'][0] for item in parent.tv.selection()]
        '''警告視窗: 排除缺乏光譜數據工卡'''
        def warning(Ecards):
            #沒有配方的工卡
            exclusion = [e for e in Ecards if e not in parent.recipeDict.keys()]
            if exclusion:
                tk.messagebox.showinfo(title='注意', message='{}等工卡無配方、將不會排序'.format(exclusion))
            Ecards = [e for e in Ecards if e not in exclusion]
            #染劑沒光譜的工卡
            exclusion = [e for e in Ecards if set(parent.recipeDict[e].dyes) - set(controller.Dyes.keys())] 
            if exclusion:
                tk.messagebox.showinfo(title='注意', message='{}等工卡無染劑光譜數據、將不會排序'.format(exclusion))
            Ecards = [e for e in Ecards if e not in exclusion]
            return Ecards
        Ecards = warning(Ecards)   
        sortresult = app_colorPermutation(Ecards,parent.recipeDict,controller.Dyes)
        ColorPermutationTable(self,sortresult)    
#工卡排序表格
class ColorPermutationTable:	
    def __init__(self,root,result):
        lst = result.lst
        
        # Create a frame to put the VerticalScrolledFrame inside
        holder_frame = tk.Frame(root)
        holder_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        # Create the VerticalScrolledFrame
        vs_frame = VerticalScrolledFrame(holder_frame)
        vs_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.TRUE)
        
        total_rows = len(lst)
        column = ['工卡','顏色','色差','配方']
        widths = [18,30,8,80]
        inds = [0,1,7,8]
        for c,w,i in zip(column,widths,inds):
            self.e = tk.Label(vs_frame.interior,
                           text=c,
                           width=w,
                           relief="ridge",
                           borderwidth=2,)
            if i==1:
                self.e.grid(row=0,column=i,columnspan=6,sticky='ew')
            else:
                self.e.grid(row=0,column=i,sticky='ew')
        total_columns = len(column) 
        for i in range(total_rows):
            for j in range(total_columns):
                if j==1:
                    if lst[i][j]:
                        #1種色cs=6; 2種色c2=3; 3種色c3=2
                        cs = 6//(3-lst[i][j].count([]))
                        m2rgb = {}
                        for k,m in enumerate(['T','N','D']):
                            if lst[i][j][k]:
                                m2rgb[m] = RGB2Hex(LAB2RGB(lst[i][j][k]))
                        for k,m in enumerate(m2rgb.keys()):
                            self.e = tk.Label(vs_frame.interior,
                                           text=m,
                                           height=1,
                                           bg=m2rgb[m],
                                           font=('Arial',16,'bold'),
                                           relief="ridge",
                                           borderwidth=2,
                                           anchor='c')
                            for l in [1,3,5]:
                                if m2rgb[m][l:l+2]>'60':
                                    break
                            else:
                                self.e.config(fg='#FFF')
                            self.e.grid(row=i+1, column=j+cs*k, columnspan=cs,sticky='nsew')
                else:
                    self.e = tk.Label(vs_frame.interior,
                                   text=lst[i][j],
                                   height=2,
                                   fg='blue',
                                   #font=('Arial',16,'bold'),
                                   relief="ridge",
                                   borderwidth=2,
                                   anchor='w')
                    if j==0:
                        self.e.grid(row=i+1,column=j,sticky='ew')
                    else:
                        self.e.grid(row=i+1,column=j+5,sticky='ew')

                
                    
        