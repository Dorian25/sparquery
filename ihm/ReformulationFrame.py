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
from nlquery.rules.utils_rules import readSuggestions

class ReformulationFrame(Frame):
    
    def __init__(self, parent):
        
        #Boolean
        self.isS1Select = False
        self.isS2Select = False
        self.isPropertySelect = False
        self.isSkeletonSelect = False
        
        self.countSubj = 0
        self.id_s1 = ""
        self.s1 = ""
        self.id_s2 = ""
        self.s2 = ""
        self.prop = ""
        self.reformulateQuestion = ""
        
        self.wd = WikiData()
        self.querySkeletons = []
        
        #Style
        s_Frame = Style()
        s_Frame.configure("Suggestions.TFrame", background="#EBECEE")
                                                        
        s_blocs = Style()
        s_blocs.configure('SuggestionsBloc.TFrame', background = 'white')
                                                                  
        s_labels= Style()
        s_labels.configure('SuggestionsLabelText.TLabel', font=("Arial", 16, 'bold'),
                                                      foreground="black",
                                                      background='white',
                                                      justify=LEFT,
                                                      anchor=W)
        s_qlabels= Style()
        s_qlabels.configure('SuggestionsQLabelText.TLabel', font=("Arial", 16, 'bold'),
                                                      foreground="black",
                                                      background='white',
                                                      justify=LEFT,
                                                      anchor=CENTER)
                              
        ##############################################                     
        
        super().__init__(parent, style="Suggestions.TFrame")  
        self.pack(fill=BOTH)                   
                              
        ##############################################
                              
        #bloc Subject
        self.blocSubject1 = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocSubject1.pack(fill=X, padx=50, pady=20)
        
        self.labelSubject1 = Label(self.blocSubject1, text="Subject 1", style="SuggestionsLabelText.TLabel")
        self.comboboxSubject1 = Combobox(self.blocSubject1, state="disabled")
        self.comboboxSubject1.bind('<<ComboboxSelected>>', self.validateSelSubject1)
        
        self.labelSubject1.pack(side=LEFT, padx=25, pady=15)
        self.comboboxSubject1.pack(side=LEFT, padx=45, fill=X, expand=True)
        
        self.blocSubject2 = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocSubject2.pack(fill=X, padx=50, pady=20)
        
        self.labelSubject2 = Label(self.blocSubject2, text="Subject 2", style="SuggestionsLabelText.TLabel")
        self.comboboxSubject2 = Combobox(self.blocSubject2, state="disabled")
        self.comboboxSubject2.bind('<<ComboboxSelected>>', self.validateSelSubject2)
        
        self.labelSubject2.pack(side=LEFT, padx=25, pady=15)
        self.comboboxSubject2.pack(side=LEFT, padx=45, fill=X, expand=True)
        ############################################## 
        
        #bloc Property
        self.blocProperty = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocProperty.pack(fill=X, padx=50, pady=20)
        
        self.labelProperty = Label(self.blocProperty, text="Property", style="SuggestionsLabelText.TLabel")
        self.comboboxProperty = Combobox(self.blocProperty,state="disabled")
        self.comboboxProperty.bind('<<ComboboxSelected>>', self.validateSelProperty)
        
        self.labelProperty.pack(side=LEFT, padx=25, pady=15)
        self.comboboxProperty.pack(side=LEFT, padx=45, fill=X, expand=True)
        
        ############################################## 
        
        #bloc Skeleton query
        self.blocQueryType = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocQueryType.pack(fill=X, padx=50, pady=20)
        
        self.labelQueryType = Label(self.blocQueryType, text="Query type", style="SuggestionsLabelText.TLabel")
        self.comboboxQueryType = Combobox(self.blocQueryType, state="disabled")
        self.comboboxQueryType.bind('<<ComboboxSelected>>', self.validateSelSkeleton)
        
        self.labelQueryType.pack(side=LEFT, padx=25, pady=15)
        self.comboboxQueryType.pack(side=LEFT, padx=45, fill=X, expand=True)
        ############################################## 
        
        #bloc Question
        self.blocQuestion = Frame(self, style="SuggestionsBloc.TFrame")
        self.blocQuestion.pack(fill=X, padx=50, pady=20)
        
        self.questionText = StringVar()
        
        self.questionLabel = Entry(self.blocQuestion, textvariable = self.questionText, font=("Arial", 16, 'bold'))
        self.questionLabel.configure(state='readonly')
        self.questionLabel.pack(fill=BOTH, pady=5)
        self.questionText.set("No question was built")

        
    def resetCombobox(self) :
        
        self.comboboxSubject1.configure(values=[],state="disabled")
        self.comboboxSubject1.set('')
        self.comboboxSubject2.configure(values=[],state="disabled")
        self.comboboxSubject2.set('')
        self.comboboxProperty.configure(values=[],state="disabled")
        self.comboboxProperty.set('')
        self.comboboxQueryType.configure(values=[],state="disabled")
        self.comboboxQueryType.set('')
        
        self.isS1Select = False
        self.isS2Select = False
        self.isPropertySelect = False
        self.isSkeletonSelect = False
        self.reformulateQuestion = ""
        self.countSubj = 0
        
        self.questionText.set("No question was built")
        
        
    def setMaterialsReformulation(self, suggestions) :
        
        self.resetCombobox()
        
        emptyS1 = True
        emptyS2 = True
        
        #seulement les subjects qui ont matché à 100%
        if suggestions["subject"] :
            
            values = [l+" ("+i+")" for i,l,d in suggestions["subject"]]
        
            self.comboboxSubject1.configure(values=values,state="normal")
            emptyS1 = False
            
            self.countSubj += 1
            
            
        if suggestions["subject1"] :
            
            values = [l+" ("+i+")" for i,l,d in suggestions["subject1"]]
            
            self.comboboxSubject1.configure(values=values,state="normal")
            emptyS1 = False
            
            self.countSubj += 1
            
            
        if suggestions["subject2"] :
            
            values = [l+" ("+i+")" for i,l,d in suggestions["subject2"]]
            
            self.comboboxSubject2.configure(values=values,state="normal")
            emptyS2 = False
            
            self.countSubj += 1
            
            
        if emptyS1 :
            self.comboboxSubject1.configure(state="disabled")
        if emptyS2 :
            self.comboboxSubject2.configure(state="disabled")
            
        self.querySkeletons = readSuggestions()
        
        
        
    def validateSelSubject1(self,event) :
        self.isS1Select = True
        
        current = self.comboboxSubject1.current()
        value = self.comboboxSubject1["values"][current]
        self.id_s1 = value[value.find("(")+1:value.find(")")]
        self.s1 = value.split(" (")[0]
        
        if self.countSubj == 1 :
            self.comboboxProperty.configure(values=["------"]+self.wd._get_all_property_of_subj(self.id_s1),state="normal")
            
        
        
    def validateSelSubject2(self,event) :
        self.isS2Select = True
        
        current = self.comboboxSubject2.current()
        value = self.comboboxSubject2["values"][current]
        self.id_s2 = value[value.find("(")+1:value.find(")")]
        self.s2 = value.split(" (")[0]
        
        print("current:", current, "value:", value)
        
        #on peut lister les propriétés relatives au(x) sujet(s)
        
        if self.isS1Select == True :
           #il faut trouver les propriétés communes aux 2 sujets
           set_prop_s1 = set(self.wd._get_all_property_of_subj(self.id_s1))
           set_prop_s2 = set(self.wd._get_all_property_of_subj(self.id_s2))
           
           compareProp = ['taller','higher','lower','shorter','smaller','less','bigger','alive','dead']
           
           self.comboboxProperty.configure(values=list(set_prop_s1.intersection(set_prop_s2))+compareProp, state="normal")
           
              
    
    def validateSelProperty(self,event) :
        self.isPropertySelect = True
        
        current = self.comboboxProperty.current()
        value = self.comboboxProperty["values"][current]
        self.prop = value
        
        print("current:", current, "value:", value)
        
        skeletons = []
        
        #on peut lister les questions compatibles avec le nombre de sujet 
        
        if self.countSubj == 1 :
            print(self.countSubj)
            if value == "------" :
                #squelettes sans (P)
                for s in self.querySkeletons :
                    if "(P)" not in s :
                        skeletons.append(s)
            else :
                #squelettes avec (P) et (S)
                for s in self.querySkeletons :
                    print(s)
                    if "(P)" in s and "(S)" in s :
                        skeletons.append(s)
                
        else : 
            #seulement les squelettes avec (S1) et (S2)
            for s in self.querySkeletons :
                    if "(S1)" in s and "(S2)" in s :
                        skeletons.append(s)
            
        if skeletons :
            self.comboboxQueryType.configure(values=skeletons, state="normal")
            
                
        
    def validateSelSkeleton(self,event) :
        self.isSkeletonSelect = True
        
        current = self.comboboxQueryType.current()
        value = self.comboboxQueryType["values"][current]
        self.reformulateQuestion = value
        
        print("current:", current, "value:", value)
        
        if (self.isS1Select or self.isS2Select) and self.isPropertySelect and self.isSkeletonSelect :
            if self.isS1Select and self.isS2Select :
                self.reformulateQuestion = self.reformulateQuestion.replace("(S1)",self.s1).replace("(S2)",self.s2)
            else :
                self.reformulateQuestion = self.reformulateQuestion.replace("(S)",self.s1)
            if self.prop != "------" :
                self.reformulateQuestion = self.reformulateQuestion.replace("(P)",self.prop)
                
            self.questionText.set(self.reformulateQuestion)
        
        
        
        
        
        