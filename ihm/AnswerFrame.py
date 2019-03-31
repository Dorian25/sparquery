# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:12:15 2019

@author: Dorian
"""


from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import urllib.request as url
import os

class AnswerFrame(Frame):
    
    def __init__(self, parent):
        
        #Style
        s_Frame= Style()
        s_Frame.configure("Answer.TFrame", background="#EBECEE")
                          
        s_answerLabel= Style()
        s_answerLabel.configure('AnswerLabel.TLabel', font=("Arial", 16, 'bold'),
                                                      foreground="#0093FC",
                                                      background="white", 
                                                      anchor = CENTER,
                                                      justify = LEFT,
                                                      wraplength=1000)
                              
        s_blocAnswer= Style()
        s_blocAnswer.configure('AnswerBloc.TFrame', background = 'white')
        
        s_blocFeed= Style()
        s_blocFeed.configure('FeedbackBloc.TFrame', background = 'white')
        
        s_labelFeedImage= Style()
        s_labelFeedImage.configure('FeedbackLabelImage.TLabel', background='white')
                                                      
        
        s_labelFeedTxt= Style()
        s_labelFeedTxt.configure('FeedbackLabelText.TLabel', font=("Arial", 16, 'bold'),
                                                      foreground="black",
                                                      background='white',
                                                      justify=LEFT,
                                                      anchor = W)
                              
        ##############################################                     
        
        super().__init__(parent, style="Answer.TFrame")  
        self.pack(fill=BOTH)                   
                              
        ##############################################
                              
        #bloc Answer
        self.blocAnswer = Frame(self, style="AnswerBloc.TFrame")
        self.blocAnswer.pack(fill=X, padx=50, pady=20)
        
        self.answerText = StringVar()
        
        self.answerLabel = Label(self.blocAnswer, textvariable = self.answerText, style="AnswerLabel.TLabel")
        self.answerLabel.pack(fill=BOTH, pady=5)
        self.answerText.set("Empty field")
        
        self.tmpJpg = "ihm/tmp/tmp_file.jpg"
        self.tmpSvg = "ihm/tmp/tmp_file.svg"
        
        self.filenameJPG = "ihm/result_image/resultat_image.jpg"
        self.filenamePNG = "ihm/result_image/resultat_image.png"
        
        ############################################## 
        
        #bloc Feedback
        self.blocFeedback = Frame(self, style="FeedbackBloc.TFrame")
        self.blocFeedback.pack(fill=X, padx=50, pady=20)
        
        self.pathFeedback = "ihm/software_image/feedback.png"
        self.imageF = Image.open(self.pathFeedback)
        self.photoF = ImageTk.PhotoImage(self.imageF)  
        self.imageFeedback = Label(self.blocFeedback, image = self.photoF, style="FeedbackLabelImage.TLabel")
        self.imageFeedback.image = self.photoF # keep a reference!
        self.imageFeedback.pack(side=LEFT)
        
        
        self.feedbackText = StringVar()
        self.labelFeedback = Label(self.blocFeedback, textvariable= self.feedbackText, style="FeedbackLabelText.TLabel")
        self.labelFeedback.pack(side=LEFT, expand=1, fill=X, padx=15)
        self.feedbackText.set("For any feedback, please ask me a question")
        
    def setFeedback(self, feedback) :
        return 0

    #ne pas oublier le format png   
    def setAnswer(self, answer, feedback):
        if answer == "None" :
            self.answerLabel.image = None
            self.answerText.set("No Answer")
            
            self.feedbackText.set("\n".join(feedback.values()))
        else :
            listAnswers = []
            multi = False
            
            if "," in answer :
                listAnswers = answer.split(",")
                multi = True
            #plusieurs réponses separees par des virgules
            if multi :
                #la réponse est une image
                if listAnswers[0].startswith("http") and (listAnswers[0].endswith("jpg") or listAnswers[0].endswith("svg")) :
                    if listAnswers[0].endswith("svg") :
                        #on telecharge l'image et l'on sauvegarde temporairement
                        url.urlretrieve(listAnswers[0], self.tmpSvg)
                        
                        #on convertit l'image svg en png
                        os.system("convert %s %s" % (self.tmpSvg, self.filenamePNG))
                        
                        img = Image.open(self.filenamePNG)
                        #https://opensource.com/life/15/2/resize-images-python
                        basewidth = 200
                        wpercent = (basewidth / float(img.size[0]))
                        hsize = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                        img.save(self.filenamePNG)
                        
                        photo = ImageTk.PhotoImage(img)
                        
                        self.answerLabel.configure(image=photo)
                        self.answerLabel.image = photo # keep a reference
                        self.feedbackText.set("\n".join(feedback.values()))
                    else :
                        #on telecharge l'image et l'on sauvegarde temporairement
                        url.urlretrieve(listAnswers[0], self.tmpJpg)
                        
                        img = Image.open(self.tmpJpg)
                        #https://opensource.com/life/15/2/resize-images-python
                        basewidth = 200
                        wpercent = (basewidth / float(img.size[0]))
                        hsize = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                        img.save(self.filenameJPG)
                        
                        photo = ImageTk.PhotoImage(img)
                        
                        self.answerLabel.configure(image=photo)
                        self.answerLabel.image = photo # keep a reference
                        self.feedbackText.set("\n".join(feedback.values()))
                        
                #la réponse est du texte
                else :
                    self.answerLabel.image = None
                    self.answerText.set(",".join(listAnswers))
                    self.feedbackText.set("\n".join(feedback.values()))
            else :
                #la réponse est une image
                if answer.startswith("http") and (answer.endswith("jpg") or answer.endswith("svg")) :
                    if answer.endswith("svg") :
                        #on telecharge l'image et l'on sauvegarde temporairement
                        url.urlretrieve(answer, self.tmpSvg)
                        
                        #on convertit l'image svg en png
                        os.system("convert %s %s" % (self.tmpSvg, self.filenamePNG))
                        
                        img = Image.open(self.filenamePNG)
                        #https://opensource.com/life/15/2/resize-images-python
                        basewidth = 200
                        wpercent = (basewidth / float(img.size[0]))
                        hsize = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                        img.save(self.filenamePNG)
                        
                        photo = ImageTk.PhotoImage(img)
                        
                        self.answerLabel.configure(image=photo)
                        self.answerLabel.image = photo # keep a reference
                        self.feedbackText.set("\n".join(feedback.values()))
                    else :
                        #on telecharge l'image et l'on sauvegarde temporairement
                        url.urlretrieve(answer, self.tmpJpg)
                        
                        img = Image.open(self.tmpJpg)
                        #https://opensource.com/life/15/2/resize-images-python
                        basewidth = 200
                        wpercent = (basewidth / float(img.size[0]))
                        hsize = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                        img.save(self.filenameJPG)
                        
                        photo = ImageTk.PhotoImage(img)
                        
                        self.answerLabel.configure(image=photo)
                        self.answerLabel.image = photo # keep a reference
                        self.feedbackText.set("\n".join(feedback.values()))
                        
                #la réponse est du texte
                else :
                    self.answerLabel.image = None
                    self.answerText.set(answer)
                    
                    self.feedbackText.set("\n".join(feedback.values()))
                    
                
                