# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:24:50 2019

@author: Dorian
"""

from tkinter import *
from tkinter.ttk import *
from .rules import all_rules
from PIL import Image, ImageTk

class ListRulesFrame(LabelFrame):
    
    def __init__(self, parent, t):
        super().__init__(parent, text = t)
        self.parent = parent
        
        self.pack()
        
        self.listBox = Listbox(self, activestyle='none', bd=0)
        for k,v in all_rules.items() :
            self.listBox.insert('end',"Rule " + k)
            
        self.listBox.bind('<<ListboxSelect>>', self.showImage)

        self.listBox.pack(fill=BOTH, expand=True)
        
    def showImage(self,evt):
        # Note here that Tkinter passes an event object
        w = evt.widget
        
        index = int(w.curselection()[0])
        value = w.get(index)
        numberRule = value.split(" ")[1].replace(".","_")
        
        window = Toplevel(self.parent)
        
        filename = "ihm/rules_image/rule-%s.png"%numberRule
        image = Image.open(filename)
        photo = ImageTk.PhotoImage(image)
        
        label = Label(window, image=photo)
        label.image = photo # keep a reference
        label.pack(fill=BOTH)
        
        



    