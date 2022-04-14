# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:10:00 2022

@author: A90127
"""

import tkinter as tk
from tkinter import filedialog

from app_GUI import GUI
from readme import frame_styles
from DyesDataBuild import specDict

class dataPage(GUI):  # 繼承GUI
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.name = 'dataPage'

        frame = tk.LabelFrame(self, frame_styles, text="匯入")
        frame.place(relx=0.1, rely=0.45, height=75, width=800)

        button1 = tk.Button(frame, text="選擇檔案", command=lambda: Load_path(self))
        button1.grid(column=0,row=0)
        button2 = tk.Button(frame, text="匯入資料", command=lambda: Load_data(self))
        button2.grid(column=0,row=1)
        Label1 = tk.Label(frame,text='',width=100)
        Label1.grid(column=1,row=0)
        Label2 = tk.Label(frame,text='',width=100)
        Label2['fg'] = '#0000FF'
        Label2.grid(column=1,row=1)

        def Load_path(self):
            filename = filedialog.askopenfilename()
            Label1['text'] = filename
            self.path = filename
    
        def Load_data(self):
            Label2.config(text='')
            controller.Dyes = specDict(self.path)
            controller.frames['ciePlotPage'].Dyes = controller.Dyes
            controller.frames['dyeVisionPage'].Dyes = controller.Dyes
            controller.frames['hit3cupsPage'].Dyes = controller.Dyes
            m = controller.frames['ciePlotPage'].var1.get()
            ls = sorted(['']+[d for d in controller.Dyes.keys() 
                               if controller.Dyes[d].material==m])
            controller.frames['ciePlotPage'].Combobox2_1['values'] = ls
            controller.frames['ciePlotPage'].Combobox3_1['values'] = ls
            controller.frames['ciePlotPage'].Combobox4_1['values'] = ls
            m = controller.frames['dyeVisionPage'].var1.get()
            ls = sorted(['']+[d for d in controller.Dyes.keys() 
                               if controller.Dyes[d].material==m])
            controller.frames['dyeVisionPage'].cb2_2_2['values'] = ls
            controller.frames['dyeVisionPage'].cb2_2_3['values'] = ls
            controller.frames['dyeVisionPage'].cb2_2_4['values'] = ls
            m = controller.frames['dyeVisionPage'].var5.get()
            ls = sorted(['']+[d for d in controller.Dyes.keys() 
                               if controller.Dyes[d].material==m])
            controller.frames['dyeVisionPage'].cb3_2['values'] = ls
            controller.frames['dyeVisionPage'].cb3_3['values'] = ls
            controller.frames['dyeVisionPage'].cb3_4['values'] = ls
            m = controller.frames['hit3cupsPage'].var1.get()
            ls = sorted(['']+[d for d in controller.Dyes.keys() 
                               if controller.Dyes[d].material==m])
            controller.frames['hit3cupsPage'].cb1_2['values'] = ls
            controller.frames['hit3cupsPage'].cb1_3['values'] = ls
            controller.frames['hit3cupsPage'].cb1_4['values'] = ls
            
            Label2.config(text='資料已匯入')
            
