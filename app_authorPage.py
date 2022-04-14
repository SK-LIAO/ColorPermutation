# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 08:09:59 2022

@author: A90127
"""

import tkinter as tk

from app_GUI import GUI
from readme import RM, frame_styles

class authorPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.name = 'authorPage'
        
        frame1 = tk.LabelFrame(self, frame_styles, text="開發說明")
        frame1.place(relx=0.15, rely=0.02, height=550, width=750)
        
        label1 = tk.Label(frame1, font=("Verdana", 12), text=RM,bg='#BEB2A7')
        label1.pack(side="top")
        
