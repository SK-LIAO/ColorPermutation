# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 08:01:21 2022

@author: A90127
"""

import tkinter as tk
import tkinter.messagebox

from app_dataPage import dataPage
from app_ciePlotPage import ciePlotPage
from app_dyeRevisePage import dyeRevisePage
from app_dyeVisionPage import dyeVisionPage
from app_authorPage import authorPage
from app_3cupsPage import hit3cupsPage


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        main_frame = tk.Frame(self, bg="#84CEEB")
        #main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        #main_frame.grid_rowconfigure(0, weight=1)
        #main_frame.grid_columnconfigure(0, weight=1)
        
        self.resizable(0, 0) #禁止調整視窗大小
        self.geometry("1024x600+504+20") #調整視窗大小及位置
        self.iconbitmap('LC.ico') 
        
        self.frames = {} #準備收集所有框架
        self.data = [] #準備放置基礎數據
        self.Dyes = {} #放置染劑字典
        self.Dyes[''] = None
        #製作各頁面
        pages = (dataPage,ciePlotPage,dyeVisionPage,hit3cupsPage,dyeRevisePage,authorPage)
        for i,F in enumerate(pages):
            frame = F(main_frame, self) #建立框架
            self.frames[frame.name] = frame #將框架存入 self 裡
            frame.grid(row=0, column=0, sticky="nsew") #放置框架
        
        #製作功能表
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)
        
        #將指定的框架拉到最上層
        self.show_frame('dataPage') 
    
    #顯示頁面函數
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise() 
    #跳出App函數
    def Quit_application(self):
        self.destroy()
        
    def Is_float(self,P):
        if P in ['','-']:
            return True
        else:
            try:
                float(P)
                return True
            except:
                return False

        
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="檔案", menu=menu_file)
        menu_file.add_command(label="匯入資料", command=lambda: parent.show_frame('dataPage'))
        menu_file.add_separator() #分隔線
        menu_file.add_command(label="離開", command=lambda: parent.Quit_application())

        menu_analysis = tk.Menu(self, tearoff=0)
        self.add_cascade(label="分析", menu=menu_analysis)
        menu_analysis.add_command(label='混色空間', command=lambda: parent.show_frame('ciePlotPage'))
        menu_analysis.add_command(label='染色視覺化',command=lambda: parent.show_frame('dyeVisionPage'))
        menu_analysis.add_command(label='模擬調修',command=lambda: parent.show_frame('hit3cupsPage'))
        menu_analysis.add_command(label='實際調修', command=lambda: parent.show_frame('dyeRevisePage'))

        menu_expression = tk.Menu(self, tearoff=0)
        self.add_cascade(label="說明", menu=menu_expression)
        menu_expression.add_command(label="關於App", command=lambda: parent.show_frame('authorPage'))

     
root = MyApp()
root.title("利勤打色研究App")

root.mainloop()