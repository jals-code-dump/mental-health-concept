# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:32:32 2021

This module takes the previous mental health scores and adds post event 
scores based on the following logic:
    
deployment - +0-2 GAD, + 0-2 PHQ
divorce - +0-1 GAD, + 0-2 PHQ
change of job - +0-1 GAD,  +/- 0-1 PHQ
moving house - +1-2 GAD, +/- 0-1 PHQ
routine - +/- 0-1 GAD/PHQ
children - +0-2 GAD, +/- 0-1 PHQ
intensity - +0-2 GAD, +/- 0-1 PHQ

This module has been written in the simplest possible manner to ease 
understanding

@author: alex counihan
"""

#import dependencies
import pandas as pd
from random import randint

#load the dataset
base_df = pd.read_csv("datasets/GAD-PHQ Dataset.csv")

#create columns for snythesised post trigger scores
base_df[['post trigger phq1', 'post trigger phq2', 'post trigger phq3',
        'post trigger phq4', 'post trigger phq5', 'post trigger phq6',
        'post trigger phq7', 'post trigger phq8', 'post trigger phq9',
        'post trigger gad1', 'post trigger gad2', 'post trigger gad3',
        'post trigger gad4', 'post trigger gad5', 'post trigger gad6',
        'post trigger gad7']] = 0

#iterate through dataset, identifying triggers and modifying scores according
#to the pre-defined logic
for index, row in base_df.iterrows():
    trigger = row['trigger']
    phq_scores = row[2:11]
    gad_scores = row[11:18]

    #get trigger phq modifiers - default is routine
    phq_min = -1
    phq_max = 1

    if trigger == 'deployment':
        phq_min = 0
        phq_max = 2

    if trigger == 'divorce':
        phq_min = 0
        phq_max = 2

    if trigger == 'change of job':
        phq_min = -1
        phq_max = 1

    if trigger == 'moving house':
        phq_min = -1
        phq_max = 1

    if trigger == 'children':
        phq_min = -1
        phq_max = 1

    if trigger == 'intensity':
        phq_min = -1
        phq_max = 1

    #get trigger gad modifiers - default is routine
    gad_min = -1
    gad_max = +1
    
    if trigger == 'deployment':
        gad_min = 0
        gad_max = 2

    if trigger == 'divorce':
        gad_min = 0
        gad_max = 1

    if trigger == 'change of job':
        gad_min = 0
        gad_max = 1

    if trigger == 'moving house':
        gad_min = 0
        gad_max = 2

    if trigger == 'children':
        gad_min = 0
        gad_max = 2

    if trigger == 'intensity':
        gad_min = 0
        gad_max = 2
    

    #modify phq scores
    for i, v in enumerate(phq_scores):
        phq_scores[i] = v + randint(phq_min, phq_max)
        
    #clean values to ensure they remain in 0-3 range
        if phq_scores[i] > 3:
            phq_scores[i] = 3
            
        if phq_scores[i] < 0:
            phq_scores[i] = 0
    
    #modify gad scores
    for i, v in enumerate(gad_scores):
        gad_scores[i] = v + randint(gad_min, gad_max)
        
    #clean values to ensure they remain in 0-3 range
        if gad_scores[i] > 3:
            gad_scores[i] = 3
            
        if gad_scores[i] < 0:
            gad_scores[i] = 0

    #store phq scores
    for i, v in enumerate(phq_scores):
        base_df.iat[index, 19 + i] = v

    
    #store gad scores
    for i, v in enumerate(gad_scores):
        base_df.iat[index, 28 + i] = v
        
#save dataset
base_df.to_csv("datasets/synth_gad-phq.csv")
