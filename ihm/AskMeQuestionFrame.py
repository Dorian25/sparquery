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
        ##############################################
        #Style
        s_Frame = Style()
        s_Frame.configure("AskFrame.TFrame",background="#22303D")
        
        ##############################################
        
        super().__init__(parent, style="AskFrame.TFrame")
        self.pack(fill=X, ipadx=15, ipady=20)
        
        ##############################################
        
        self.inputText = Entry(self, font=("Verdana", 15))
        #placeholder
        self.inputText.insert(0, "Ask me a question...")
        
        self.inputText.bind('<FocusIn>', self.delete)
        self.inputText.bind('<Return>',self.askMe)
        
        self.inputText.pack(fill=X, expand=True, padx=50, ipady=2)
        
        ##############################################
        self.answerCorrect = StringVar()
        
        self.blocCorrect = Frame(self)
        self.blocCorrect.pack(fill=X, side=BOTTOM)
        
        label = Label(self.blocCorrect,text="Is correct answer ?")
        r1 = Radiobutton(self.blocCorrect, text="Yes", variable=self.answerCorrect, value="yes", command=self.feedbackAnswer)
        r2 = Radiobutton(self.blocCorrect, text="No", variable=self.answerCorrect, value="no", command=self.feedbackAnswer)
        
        label.pack(side=LEFT)
        r1.pack(side=LEFT)
        r2.pack(side=LEFT)
        
        ##############################################
        #Pages à update
        self.treeQuery = None
        self.treeRule = None
        self.sparqlQuery = None
        self.answer = None
        self.dictAns = None
        self.suggestion = None
        self.history = None
        
        ##############################################
        #Permet de savoir si l'utilisateur a appuyé sur ENTER
        #après avoir entrer une question
        self.pushEnter = False
        
    def feedbackAnswer(self):
        print("feedback")
        #on enregistre le feedback de l'utilisateur une fois qu'il a posé
        #sa question, c'est a dire une fois qu'il a appuyé sur ENTER
        question = self.inputText.get()
        
        if question and self.pushEnter :
            if self.dictAns['plain'] == "None":
                self.history.refreshHistory(question, "no", self.answerCorrect.get())
            else :
                self.history.refreshHistory(question, "yes", self.answerCorrect.get())                
            self.pushEnter = False
        
        self.answerCorrect.set(None)
        
    def delete(self, event):
        if self.inputText.get() == "Ask me a question..." :
            self.inputText.delete(0, "end")
        
    def askMe(self, event):
        
        inputUser = self.inputText.get()
        
        if not inputUser :
            self.pushEnter = False
            
            self.answer.setAnswer("Your question is empty", {})
        else :
            self.pushEnter = True
            
            engine = NLQueryEngine('localhost', 9000)
            self.dictAns, match_rule = engine.query(inputUser, format_='raw')
            print(self.dictAns)
            
            if not match_rule :
                self.dictAns["feedback"]["no match"] = "This type of question was not recognized by the system"
                
            self.answer.setAnswer(self.dictAns['plain'], self.dictAns["feedback"])
            self.treeQuery.setTreeQuery(self.dictAns['tree'])
            self.treeRule.setTreeQuery(match_rule)
            if 'sparql_query' in self.dictAns:
                self.sparqlQuery.setQuery(self.dictAns['sparql_query'], self.dictAns['sparql_desc'])
            else :
                self.sparqlQuery.setQuery(None, None)
            if 'suggestions' in self.dictAns:    
                self.suggestion.setSuggestion(self.dictAns['suggestions']['subject'], self.dictAns['suggestions']['prop'])
            else :
                self.suggestion.setSuggestion([],[])