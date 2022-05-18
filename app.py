# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 08:01:21 2022

@author: A90127
"""

import tkinter as tk
import tkinter.messagebox
#from tkinter import filedialog
#from tkinter import ttk
#from pyperclip import copy

from app_dataPage import DataBuildPage
from app_mainPage import MainPage
from app_authorPage import AuthorPage
from app_dyemachinePage import DyeMachinePage

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        main_frame = tk.Frame(self, bg="#84CEEB")
        main_frame.pack(fill="both", expand="true")
        
        self.resizable(0, 0) #禁止調整視窗大小
        self.geometry("1024x600+504+20") #調整視窗大小及位置
        self.iconbitmap('LC.ico') 
        
        #準備製作各子頁面
        self.frames = {} #收集所有框架用       
        pages = (DataBuildPage,MainPage,DyeMachinePage,AuthorPage)
        for F in pages:
            frame = F(main_frame, self) #建立框架
            self.frames[F] = frame #將框架存入 self 裡
            frame.grid(row=0, column=0, sticky="nsew") #放置框架
        
        #製作功能表
        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)
        
        #將指定的框架拉到最上層
        self.show_frame(DataBuildPage)
    
    #顯示頁面函數
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise() 
    #跳出App函數
    def Quit_application(self):
        self.destroy()
    
        
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="檔案", menu=menu_file)
        menu_file.add_command(label="匯入資料", command=lambda: parent.show_frame(DataBuildPage))
        menu_file.add_separator() #分隔線
        menu_file.add_command(label="離開", command=lambda: parent.Quit_application())
        
        menu_main = tk.Menu(self, tearoff=0)
        self.add_cascade(label="主程式", menu=menu_main)
        menu_main.add_command(label='分析排序', command=lambda: parent.show_frame(MainPage))
        menu_main.add_command(label='機台設定', command=lambda: parent.show_frame(DyeMachinePage))
        
        menu_expression = tk.Menu(self, tearoff=0)
        self.add_cascade(label="說明", menu=menu_expression)
        menu_expression.add_command(label="關於App", command=lambda: parent.show_frame(AuthorPage))
            
        
root = MyApp()
root.title("利勤排色App")

root.mainloop()