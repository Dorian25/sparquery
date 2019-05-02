# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 21:34:27 2019

@author: Dorian
"""

from tkinter import *
from tkinter.ttk import *
import os.path
import csv
from nlquery.wikidata import WikiData

class ReformulationFrame(Frame):
    
    def __init__(self, parent):
        
        #Boolean
        self.isPropertySelect = False
        self.isSkeletonSelect = False
        
        #Style
        s_Frame = Style()
        s_Frame.configure("Suggestions.TFrame", background="#EBECEE")
                          
        s_subjectLabel= Style()
        s_subjectLabel.configure('subjectLabel.TLabel', font=("Arial", 16, 'bold'),
                                                      foreground="#0093FC",
                                                      background="white", 
                                                      anchor = CENTER,
                                                      justify = LEFT,
                                                      wraplength=1000)
                              
        s_blocs = Style()
        s_blocs.configure('SuggestionsBloc.TFrame', background = 'white')
                                                                  
        s_labels= Style()
        s_labels.configure('SuggestionsLabelText.TLabel', font=("Arial", 16, 'bold'),
                                                      foreground="black",
                                                      background='white',
                                                      justify=LEFT,
                                                      anchor = W)
                              
        ##############################################                     
        
        super().__init__(parent, style="Suggestions.TFrame")  
        self.pack(fill=BOTH)                   
                              
        ##############################################
                              
        #bloc Subject
        self.blocSubject = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocSubject.pack(fill=X, padx=50, pady=20)
        
        self.subjectText = StringVar()
        
        self.subjectLabel = Label(self.blocSubject, textvariable = self.subjectText, style="subjectLabel.TLabel")
        self.subjectLabel.pack(fill=BOTH, pady=5)
        self.subjectText.set("No subject(s)")
        
        ############################################## 
        
        #bloc Property
        self.blocProperty = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocProperty.pack(fill=X, padx=50, pady=20)
        
        self.labelProperty = Label(self.blocProperty, text="Property", style="SuggestionsLabelText.TLabel")
        self.comboboxProperty = Combobox(self.blocProperty)
        
        self.labelProperty.pack(side=LEFT, padx=25, pady=15)
        self.comboboxProperty.pack(side=LEFT, padx=45, fill=X, expand=True)
        
        ############################################## 
        
        #bloc Skeleton query
        self.blocQueryType = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocQueryType.pack(fill=X, padx=50, pady=20)
        
        self.labelQueryType = Label(self.blocQueryType, text="Query type", style="SuggestionsLabelText.TLabel")
        self.comboboxQueryType = Combobox(self.blocQueryType)
        
        self.labelQueryType.pack(side=LEFT, padx=25, pady=15)
        self.comboboxQueryType.pack(side=LEFT, padx=45, fill=X, expand=True)
        ############################################## 
        
        #bloc Question
        self.blocQuestion = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocQuestion.pack(fill=X, padx=50, pady=20)
        
        self.questionText = StringVar()
        
        self.questionLabel = Label(self.blocQuestion, textvariable = self.questionText, style="SuggestionsLabelText.TLabel")
        self.questionLabel.pack(fill=BOTH, pady=5)
        self.questionText.set("No question was built")
        
    def setMaterialsReformulation(self, params) :
        #seulement les subjects qui ont matché à 100%
        if "subject" in params :
            self.subjectText.set(params["subject"].upper())
            
        
        self.comboboxProperty.configure(values=["prop1","prop2","prop3"])
        
        
        
        
        
        
        