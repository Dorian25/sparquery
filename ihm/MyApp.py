# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 19:48:47 2019

@author: Dorian
"""

from tkinter import *
from tkinter.ttk import *
from .TreeQueryFrame import TreeQueryFrame
from .TreeRuleFrame import TreeRuleFrame
from .SparqlQueryFrame import SparqlQueryFrame
from .AnswerFrame import AnswerFrame
from .AskMeQuestionFrame import AskMeQuestionFrame
from .DidYouMeanFrame import DidYouMeanFrame
from .HistoryFrame import HistoryFrame
from .ReformulationFrame import ReformulationFrame

class MyApp(Tk) :
    
    def __init__(self):
        super().__init__()

        self.title("Interrogation SPARQL/RDF en Langage Naturel")
        self.iconbitmap("ihm/software_image/cropped-bot-logo.ico")
        self.minsize(1200,750)
        
        ##############################################
        #Style########################################
        ##############################################
                             
        s_notebook = Style()
        s_notebook.configure("TNotebook.Tab",font=('Arial', 12, 'bold'),
                                             padding=[5,4],
                                             foreground="#22303D")
                             
        ##############################################
        #Components###################################
        ##############################################
        
        #Fenetre principale
        
        self.frameGlobal = Frame(self, style="FrameGlobal.TFrame")
        self.frameGlobal.pack(expand=True, fill=BOTH)
        
        ##############################################
        #barre de recherche
        self.askMeQuestionFrame = AskMeQuestionFrame(self.frameGlobal)
        
        ##############################################
        #Notebook permettant de naviguer a travers des onglets
        
        self.tabs = Notebook(self.frameGlobal, style="TNotebook")

        ##############################################
        #Onglet Tree parser (POS TAGGING)
        self.left = PanedWindow(self.tabs, orient = VERTICAL)
        self.left.pack()
        
        
        self.treeQueryFrame = TreeQueryFrame(self.left, "Parse Query Tree")
        self.treeRulesFrame = TreeRuleFrame(self.left, "Matched Rule Tree")
        
        self.left.add(self.treeQueryFrame)
        self.left.add(self.treeRulesFrame)
        
        ##############################################
        #Fenetre de reponse, suggetion et requete sparql
        self.answerFrame = AnswerFrame(self.tabs)
        self.sparqlFrame = SparqlQueryFrame(self.tabs)
        self.didYouMeanFrame = DidYouMeanFrame(self.tabs)
        self.historyFrame = HistoryFrame(self.tabs)
        self.reformulationFrame = ReformulationFrame(self.tabs)

        self.askMeQuestionFrame.treeQuery = self.treeQueryFrame
        self.askMeQuestionFrame.treeRule = self.treeRulesFrame
        self.askMeQuestionFrame.sparqlQuery = self.sparqlFrame
        self.askMeQuestionFrame.answer = self.answerFrame  
        self.askMeQuestionFrame.suggestion = self.didYouMeanFrame
        self.askMeQuestionFrame.history = self.historyFrame
        self.askMeQuestionFrame.reformulation = self.reformulationFrame
        
        ##############################################
        #Parametrage du notebook pour ajouter tous les onglets et les fenetres
        
        self.tabs.add(self.answerFrame, text="Answer".upper()) 
        self.tabs.add(self.sparqlFrame, text="SPARQL Query".upper())
        self.tabs.add(self.left, text="POS Tags Tree".upper())
        self.tabs.add(self.didYouMeanFrame, text="Did you mean".upper())
        self.tabs.add(self.historyFrame, text="History".upper())
        self.tabs.add(self.reformulationFrame, text="Reformulation".upper())
        #ajouter onglet Existed property (listant toutes les proprietes d'un subject)
        self.tabs.pack(expand=1, fill=BOTH) 
        
        ##############################################
        #barre de status
        #self.statusBar = Label(self,text="Welcome ", anchor=W, relief=SUNKEN, borderwidth=1)
        #self.statusBar.pack(fill=X, side=BOTTOM) 