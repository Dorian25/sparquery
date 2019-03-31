# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 13:17:18 2019

@author: Dorian
"""

from tkinter import *
from tkinter.ttk import *

    
class SparqlQueryFrame(Label):
    
    def __init__(self, parent):
        
        #Style
        s_Frame = Style()
        s_Frame.configure('SparqlQuery.TFrame', background="#EBECEE")
                          
        s_blocQuery = Style()
        s_blocQuery.configure('QueryBloc.TFrame', background = 'white')
                              
        s_LabelQuery = Style()
        s_LabelQuery.configure('QueryLabel.TLabel', background = "#EFF0F2",
                                                    foreground = "black",
                                                    font = ("courier",14),
                                                    justify=LEFT,
                                                    anchor=CENTER)
                              
        s_blocDesc = Style()
        s_blocDesc.configure('DescBloc.TFrame', background = 'white')
                
        s_Treeview = Style()
        s_Treeview.configure("tableau.Treeview", highlightthickness=0, 
                                                 bd=0, 
                                                 font=('courier', 13), 
                                                 background="#e0e0e0", 
                                                 foreground="black", 
                                                 fieldbackground="#e0e0e0") # Modify the font of the body
        s_Treeview.configure("tableau.Treeview.Heading", font=('Arial', 15)) # Modify the font of the headings
        s_Treeview.layout("tableau.Treeview", [('tableau.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
                          
        ############################################## 
        
        super().__init__(parent, style="SparqlQuery.TFrame")
        self.pack(fill=BOTH)
        
        ##############################################                         
        #bloc Query
        self.blocQuery = Frame(self, style="QueryBloc.TFrame")
        self.blocQuery.pack(fill=X, padx=50, pady=20)
        
        self.queryText = StringVar()
        
        self.queryLabel = Label(self.blocQuery, textvariable = self.queryText, style="QueryLabel.TLabel")
        self.queryLabel.pack(pady=20)
        self.queryText.set("Empty field")
        
        
        ############################################## 
        #bloc description
        self.blocDesc = Frame(self, style="DescBloc.TFrame")
        self.blocDesc.pack(fill=X, padx=50, pady=20)
        
        self.dataCols = ('id', 'label')        
        self.tableauDesc = Treeview(self.blocDesc, columns=self.dataCols, show = 'headings', style="tableau.Treeview", selectmode = "none")
        for c in self.dataCols:
            self.tableauDesc.heading(c, text=c.title())            
            self.tableauDesc.column(c, anchor=CENTER)
        self.tableauDesc.pack(fill=X)
        
    def setQuery(self, query, desc):
        
        if query == None :
            self.queryText.set("No SPARQL query")
        else :
            self.queryText.set(query)
            
            
        #on vide le tableau
        for child in self.tableauDesc.get_children():
            self.tableauDesc.delete(child)
        #on le rempli
        if desc != None :
            for k,v in desc.items():
                #insert(parent, ajoute apres)
                self.tableauDesc.insert("", 'end', values = (k,v))
   