# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 08:23:13 2022

@author: A90127
"""

from app_GUI import GUI
from readme import frame_styles, RM
from tkinter import LabelFrame
from tkinter import Label

class AuthorPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)  
        
        GUI.__init__(self, parent)        
        frame1 = LabelFrame(self, frame_styles, text="開發說明")
        frame1.place(relx=0.15, rely=0.02, height=550, width=750)       
        label1 = Label(frame1, font=("Verdana", 12), text=RM,bg='#BEB2A7')
        label1.pack(side="top")