# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 20:18:08 2019

@author: Dorian
"""

from tkinter import *
from tkinter.ttk import *
from nltk.tree import Tree
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
from PIL import Image, ImageTk
import os

class TreeRuleFrame(LabelFrame):
    
    def __init__(self,parent,t):
        super().__init__(parent,text=t)
        self.pack()
        
        self.filenamePS = "ihm/result_image/tree_rule.ps"
        self.filenamePNG = "ihm/result_image/tree_rule.png"
        self.filenameDefault = "ihm/software_image/default.png"
        
        self.image = Image.open(self.filenameDefault)
        self.photo = ImageTk.PhotoImage(self.image)
        
        self.labelTreeRule = Label(self, image = self.photo)
        self.labelTreeRule.image = self.photo # keep a reference!
        self.labelTreeRule.pack(fill=BOTH)
    
    
    def convertPsToPng(self, treeVal):
        cf = CanvasFrame()
        
        tr = Tree.fromstring(treeVal)
        tc = TreeWidget(cf.canvas(),tr)
        
        tc['node_font'] = 'arial 13 bold'
        tc['leaf_font'] = 'arial 11'
        tc['node_color'] = '#005990'
        tc['leaf_color'] = '#3F8F57'
        tc['line_color'] = '#175252'
        tc['xspace'] = 25
        tc['yspace'] = 25
        
        cf.add_widget(tc,10,10) # (10,10) offsets
        
        cf.print_to_file(self.filenamePS)
        cf.destroy()
        
        #MagickImage doit etre installée ainsi que convert
        os.system("convert %s %s" % (self.filenamePS, self.filenamePNG))
            
    def setTreeQuery(self, treeVal):
        
        #à l'ouverture de l'application ou si aucune regle n'a ete reconnue
        if not treeVal :
        
            self.image = Image.open(self.filenameDefault)
            self.photo = ImageTk.PhotoImage(self.image)
            self.labelTreeRule.configure(image=self.photo)
            self.labelTreeRule.image = self.photo # keep a reference
            
        else :
            
            self.convertPsToPng(treeVal)
            
            self.image = Image.open(self.filenamePNG)
            self.photo = ImageTk.PhotoImage(self.image)
            self.labelTreeRule.configure(image=self.photo)
            self.labelTreeRule.image = self.photo # keep a reference