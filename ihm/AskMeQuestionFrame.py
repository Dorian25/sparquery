# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:12:56 2019

@author: Dorian
"""

from tkinter import *
from tkinter.ttk import *
from nlquery.nlquery import NLQueryEngine
from PIL import Image, ImageTk

class AskMeQuestionFrame(Frame):
    
    def __init__(self, parent):
        
        #Style
        s_Input = Style()
        
        s_Frame = Style()
        s_Frame.configure("AskFrame.TFrame",background="#22303D")
        
        ##############################################
        
        super().__init__(parent, style="AskFrame.TFrame")
        self.pack(fill=X, ipadx=20, ipady=20)
        
        ##############################################
        
        self.inputText = Entry(self, font=("Verdana", 15))
        #placeholder
        self.inputText.insert(0, "Ask me a question...")
        
        self.inputText.bind('<FocusIn>', self.delete)
        self.inputText.bind('<Return>',self.askMe)
        
        self.inputText.pack(fill=X, expand=True, side=LEFT, padx=50, ipady=2)
        
        ##############################################
        
        self.treeQuery = None
        self.treeRule = None
        self.sparqlQuery = None
        self.answer = None
        self.suggestion = None
        
    def delete(self, event):
        if self.inputText.get() == "Ask me a question..." :
            self.inputText.delete(0, "end")
        
    def askMe(self, event):
        
        inputUser = self.inputText.get()
        
        if not inputUser :
            self.answer.setAnswer("Your question is empty", {})
        else :
            engine = NLQueryEngine('localhost', 9000)
            dictAns,match_rule = engine.query(inputUser, format_='raw')
            print(dictAns)
            
            self.answer.setAnswer(dictAns['plain'], dictAns["feedback"])
            self.treeQuery.setTreeQuery(dictAns['tree'])
            self.treeRule.setTreeQuery(match_rule)
            if 'sparql_query' in dictAns:
                self.sparqlQuery.setQuery(dictAns['sparql_query'], dictAns['sparql_desc'])
            else :
                self.sparqlQuery.setQuery(None, None)
                
            self.suggestion.setSuggestion(dictAns['suggestions']['subject'], dictAns['suggestions']['prop'])