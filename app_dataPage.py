# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 08:22:27 2022

@author: A90127
"""

from tkinter import LabelFrame, Button, Label, filedialog


import dataBuild as dB
from app_GUI import GUI
from readme import frame_styles


class DataBuildPage(GUI):  # 繼承GUI
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        #存放併染工卡字典
        controller.mergeE = {}
        controller.mergeE['AllChildren'] = []
        #存放讀取檔案的路徑
        self.path = ['','','','']
        
        frame1 = LabelFrame(self, frame_styles, text="匯入工卡進度")
        frame1.place(relx=0.1, rely=0.1, height=75, width=800)
        button1_1 = Button(frame1, text="選擇檔案", command=lambda: Load_path(self,0))
        button1_1.grid(column=0,row=0)
        button1_2 = Button(frame1, text="匯入資料", command=lambda: Load_data1(self))
        button1_2.grid(column=0,row=1)
        Label1_1 = Label(frame1,text='',width=100,fg='#00F')
        Label1_1.grid(column=1,row=0)
        Label1_2 = Label(frame1,text='',width=100,fg='#00F')
        Label1_2.grid(column=1,row=1)
        
        frame2 = LabelFrame(self, frame_styles, text="匯入工卡配方")
        frame2.place(relx=0.1, rely=0.3, height=75, width=800)
        button2_1 = Button(frame2, text="選擇檔案", command=lambda: Load_path(self,1))
        button2_1.grid(column=0,row=0)
        button2_2 = Button(frame2, text="匯入資料", command=lambda: Load_data2(self))
        button2_2.grid(column=0,row=1)
        Label2_1 = Label(frame2,text='',width=100,fg='#00F')
        Label2_1.grid(column=1,row=0)
        Label2_2 = Label(frame2,text='',width=100,fg='#00F')
        Label2_2.grid(column=1,row=1)
        
        frame3 = LabelFrame(self, frame_styles, text="匯入光譜數據")
        frame3.place(relx=0.1, rely=0.5, height=75, width=800)
        button3_1 = Button(frame3, text="選擇檔案", command=lambda: Load_path(self,2))
        button3_1.grid(column=0,row=0)
        button3_2 = Button(frame3, text="匯入資料", command=lambda: Load_data3(self))
        button3_2.grid(column=0,row=1)
        Label3_1 = Label(frame3,text='',width=100,fg='#00F')
        Label3_1.grid(column=1,row=0)
        Label3_2 = Label(frame3,text='',width=100,fg = '#00F')
        Label3_2.grid(column=1,row=1)
        
        frame4 = LabelFrame(self, frame_styles, text="匯入併染工卡")
        frame4.place(relx=0.1, rely=0.7, height=75, width=800)
        button4_1 = Button(frame4, text="選擇檔案", command=lambda: Load_path(self,3))
        button4_1.grid(column=0,row=0)
        button4_2 = Button(frame4, text="匯入資料", command=lambda: Load_data4(self))
        button4_2.grid(column=0,row=1)
        Label4_1 = Label(frame4,text='',width=100,fg='#00F')
        Label4_1.grid(column=1,row=0)
        Label4_2 = Label(frame4,text='',width=100,fg = '#00F')
        Label4_2.grid(column=1,row=1)
        
        def Load_path(self,i):
            filename = filedialog.askopenfilename()
            Labels = [Label1_1,Label2_1,Label3_1,Label4_1]
            Labels[i]['text'] = filename
            self.path[i] = filename
    
        def Load_data1(self):
            #回傳在染房待染工卡數據  ('工卡號','染單單號','表頭狀態','開卡量','站別','刷卡日期')等欄位數據
            controller.waitDye = dB.app_waitDye(self.path[0])
            Label1_2['text'] = '資料已匯入'
            
        def Load_data2(self):
            #回傳工卡的配方數據 ('工卡號','顏色','染劑代號','配方濃度(化驗)')等欄位數據
            controller.recipeE = dB.app_recipeE(self.path[1])
            Label2_2['text'] = '資料已匯入'

        def Load_data3(self):
            #回傳染劑稱 -> 濃度陣列 光譜陣列 的字典
            #ex Dyes['TR101'].conc Dyes['TR101'].spec
            controller.Dyes = dB.app_spectrum(self.path[2])
            Label3_2['text'] = '資料已匯入'
            
        def Load_data4(self):
            #回傳主工卡號 ->併染子工卡號陣列的字典
            #ec mergeE['E220314001']
            controller.mergeE = dB.mergeE(self.path[3])
            Label4_2['text'] = '資料已匯入'

