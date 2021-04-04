#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:05:34 2021

@author: Daniel
"""

### SPERM PREDICTOR APP v1.0 ###

#SpermAPP1.0

#import libraries
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import os
import random
import glob


###IMPORTANT###
###DEFINE YOUR PATHS HERE###

###RICARDO: muda \\ também na linha 127 e 133

#define path to test set folder here; ATTENTION: don't forget the /* (or \\* in Windows) at the end, so that it retrieves images from all subfolders/classes
path = '/Users/Daniel/Documents/DL_Project/Datasets/SCIAN-MorphoSpermGS/Partial-Agreement-Images/test/*'

#define path to dataframe of CNN predictions
df_predictions_path = '/Users/Daniel/Documents/DL_Project/Datasets/SCIAN-MorphoSpermGS/Partial-Agreement-Images/predictions.csv'

dataframe = pd.read_csv(df_predictions_path)


#defines dictionary with label:classe
dict_class = {0:'Normal', 1:'Tapered', 2:'Pyriform', 3:'Amorphous'}



class Interface(Frame):
    
    

    def update_image(self):
        
        #plots new image on top of previous one
        img.config(image=get_image())
        
        #deletes box from prediction
        var_pred = StringVar()
        label_pred = Label(self, textvariable=var_pred, justify = 'center')
        var_pred.set('')
        label_pred.place(x=0,y=50, width = 280, height = 50)
        
        #updates real box
        var_real = StringVar()
        label_real = Label(self, textvariable=var_real, relief=RAISED, justify = 'center', bg = 'grey')
        var_real.set('Real Label: ' + str(dict_class[real_label]))
        label_real.place(x=0,y=0, width = 280, height = 50)
        
        

    def predict_button(self):

        #chooses color of predicted box based on in/correct prediction
        if real_label == predicted_label:
            color = 'green'
        else:
            color = 'red'
        
        #creates box to show predicted label
        var_pred = StringVar()
        label_pred = Label(self, textvariable=var_pred, relief=RAISED, justify = 'center', bg = color)
        var_pred.set('Predicted Label: ' + str(dict_class[predicted_label]))
        label_pred.place(x=0,y=50, width = 280, height = 50)
        
        
        
    def __init__(self, master=None):
        
        global img
        
        #creates interface
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        
        #plots current image
        img = tkinter.Label(self, image=get_image(), compound='bottom')
        img.image = render
        img.place(x=0, y=100)
        
        #creates boxes for future predictions
        var_real = StringVar()
        label_real = Label(self, textvariable=var_real, relief=RAISED,  justify = 'center', bg = 'grey')
        var_real.set('Real Label: ' + str(dict_class[real_label]))
        label_real.place(x=0,y=0, width = 280, height = 50)
        
        #creates predict and next buttons
        button_predict = tkinter.Button(self, text ="Predict", font=('Arial', 15), command = self.predict_button).place(x=0,y=400, width = 140, height = 50)
        button_next = tkinter.Button(self, text ="Next Image", font=('Arial', 15), command = self.update_image).place(x=140,y=400, width = 140, height = 50)



def get_image():
    
        global render, real_label, predicted_label
        
        #imports random image from entire dataset
        file_path_type = [path + "/*.tif"] ###CHANGE HERE / to \\
        dataset_all = glob.glob(random.choice(file_path_type))
        random_image = random.choice(dataset_all)
        
        ###THIS WILL BE ELIMINATED ONCE THE #SpermAPP PERFORMS PREDICTIONS IN REAL TIME###
        #stores filename of randomly chosen image
        image_filename = random_image.split('/')[-2]+'/'+random_image.split('/')[-1] ###CHANGE HERE / to \\
        
        #loads random image from repository
        load = Image.open(random_image)
        load = load.resize((280, 280), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        
        #gets label of chosen image
        real_label = dataframe[dataframe['Filename'] == image_filename]['Label'].values[0]
        predicted_label  = dataframe[dataframe['Filename'] == image_filename]['AlexNet'].values[0]

        return render
        
        

#calls root, initializes interface
root = Tk()
app = Interface(root)
root.wm_title("CNN Sperm Class Predictor")
root.geometry("285x460")
root.mainloop()

