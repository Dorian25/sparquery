# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 22:31:21 2019

@author: Dorian
"""

from tkinter import *
from tkinter.ttk import *

    
class DidYouMeanFrame(Label):
    
    def __init__(self, parent):
        
        #Style
        s_Frame = Style()
        s_Frame.configure('DidYouMean.TFrame', background="#EBECEE")
                          
        s_blocSuggSubj = Style()
        s_blocSuggSubj.configure('SuggSubjBloc.TFrame', background = 'white')
                              
        s_blocSuggProp = Style()
        s_blocSuggProp.configure('SuggPropBloc.TFrame', background = 'white')
                          
        ############################################## 
        
        super().__init__(parent, style="DidYouMean.TFrame")
        self.pack(fill=BOTH)
        
        ##############################################                         
        #bloc Suggestion Subject
        self.blocSuggSubj = Frame(self, style="SuggSubjBloc.TFrame")
        self.blocSuggSubj.pack(fill=X, padx=50, pady=20)
        
        self.dataColsSubj = ('suggestion subject', 'description')        
        self.tableauSubj = Treeview(self.blocSuggSubj, columns=self.dataColsSubj, show = 'headings', style="tableau.Treeview", selectmode = "none")
        for c in self.dataColsSubj:
            self.tableauSubj.heading(c, text=c.title(), anchor=CENTER)            
            self.tableauSubj.column(c)
        self.tableauSubj.pack(expand=True,side=LEFT,fill=X)
        
        self.vscrollbarSubj = Scrollbar(self.blocSuggSubj, command=self.tableauSubj.yview, orient="vertical")
        self.vscrollbarSubj.pack(side=LEFT,fill=Y)
        self.tableauSubj.configure(yscrollcommand=self.vscrollbarSubj.set)
    

        ############################################## 
        #bloc Suggestion prop
        self.blocSuggProp = Frame(self, style="SuggPropBloc.TFrame")
        self.blocSuggProp.pack(fill=X, padx=50, pady=20)
        
        self.dataColsProp = ('suggestion property', 'description')        
        self.tableauProp = Treeview(self.blocSuggProp, columns=self.dataColsProp, show = 'headings', style="tableau.Treeview", selectmode = "none")
        for c in self.dataColsProp:
            self.tableauProp.heading(c, text=c.title(), anchor=CENTER)            
            self.tableauProp.column(c)
        self.tableauProp.pack(expand=True,side=LEFT,fill=X)
        
        self.vscrollbarProp = Scrollbar(self.blocSuggProp, command=self.tableauProp.yview, orient="vertical")
        self.vscrollbarProp.pack(side=LEFT,fill=Y)
        self.tableauProp.configure(yscrollcommand=self.vscrollbarProp.set)
        
    def setSuggestion(self, suggSubj, suggProp):
        
        #on vide les tableaux
        for child in self.tableauSubj.get_children():
            self.tableauSubj.delete(child)
        for child in self.tableauProp.get_children():
            self.tableauProp.delete(child)
            
        #on les rempli
        if suggSubj :
            for s in suggSubj:
                #insert(parent, ajoute apres)
                self.tableauSubj.insert("", 'end', values = (s[0],s[1]))
        if suggProp :
            for s in suggProp:
                #insert(parent, ajoute apres)
                self.tableauProp.insert("", 'end', values = (s[0],s[1]))                