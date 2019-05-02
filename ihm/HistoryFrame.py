# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:24:40 2019

@author: Dorian
"""


from tkinter import *
from tkinter.ttk import *
import os.path
import csv

    
class HistoryFrame(Label):
    
    
    def __init__(self, parent):
        self.filepath = "ihm/history/log_history.csv"
        
        #Style
        s_Frame = Style()
        s_Frame.configure('History.TFrame', background="#EBECEE")
                          
        s_blocHistory = Style()
        s_blocHistory.configure('HistoryBloc.TFrame', background = 'white')
                                                        
        ############################################## 
        
        super().__init__(parent, style="History.TFrame")
        self.pack(fill=BOTH)
        
        ##############################################                         
        #bloc Suggestion Subject
        self.blocHistory = Frame(self, style="HistoryBloc.TFrame")
        self.blocHistory.pack(fill=X, padx=50, pady=20)
        
        self.columns = ('question', 'answered', 'correct')        
        self.tableauHistory = Treeview(self.blocHistory, columns=self.columns, show = 'headings', style="tableau.Treeview", selectmode = "none")
        for c in self.columns:
            self.tableauHistory.heading(c, text=c.title(), anchor=CENTER)            
            self.tableauHistory.column(c)
        self.tableauHistory.pack(expand=True,side=LEFT,fill=X)
        
        self.vscrollbar = Scrollbar(self.blocHistory, command=self.tableauHistory.yview, orient="vertical")
        self.vscrollbar.pack(side=LEFT,fill=Y)
        self.tableauHistory.configure(yscrollcommand=self.vscrollbar.set)
        
        self.loadHistory()
            

    def refreshHistory(self, question, status, correct):
        #on ajoute une nouvelle ligne à l'historique et 
        #on l'ajoute au tableau      
        
        #delimiter "," par defaut
        row = [question,status,correct]
        
        if os.path.isfile(self.filepath) :
            #append mode = permet d'ajouter à un fichier existant
            with open(self.filepath, 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                
                writer.writerow(row)
                
            csvFile.close()
        else :
            with open(self.filepath, 'w', newline='') as csvFile:
                writer = csv.writer(csvFile)
                
                writer.writerow(row)
                
            csvFile.close()
                    
        self.tableauHistory.insert("", 'end', values = (question,status,correct))
        
        
        
    def loadHistory(self):
        #on charge le fichier lorsque l'appli s'ouvre
        
        #si le fichier de log existe alors on le lit et rempli le tableau
        if os.path.isfile(self.filepath) :
            print("exist")
            #avant d'afficher on supprime
            #delimiter "," par defaut
            with open(self.filepath, 'r') as csvFile:
                reader = csv.reader(csvFile)
                
                for row in reader:
                    if len(row) != 0 :
                        print("row",row)
                        self.tableauHistory.insert("", 'end', values = (row[0],row[1],row[2]))

            csvFile.close()