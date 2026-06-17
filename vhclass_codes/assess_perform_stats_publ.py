# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 14:48:24 2025

@author: 334992
"""

# this code claculates parameters to assess the performance of classifier

import pandas as pd
import numpy as np

def assess_perform_stats_publ(data):
# pulls the sequence of the given id from a database file

    d = pd.read_csv(data)
    tp = tn = fp = fn = 0
# assess accuracy:
#Accuracy = (True Positives + True Negatives) / Total Predictions
    tp = 0
    tn = 0
    labels=[]
    for items in range(len(d)):
        idx_tmp = d.header[items].index('_')
    #print([d.header[items],idx_tmp])
        labels.append([d.prediction[items][0:3],d.header[items][4:7]])#-5:-2     
        ll2 = []

    ll2 = pd.DataFrame(labels,columns = ['pred','true'])     
    tt = 0
    for items in range(len(ll2)):
        if ll2.true[items] == ll2.pred[items]:
            tt+=1   
     
    acc = (tt/len(d))
# assess precision
# true positives and true negatives in the set (true labels)

    pos_true=list(ll2.true).count('hum') # actual number of positive seqs (hum)
    neg_true=list(ll2.true).count('cam')
# number of correctly identifird positives:
    tp = 0
    for items in range(len(ll2)):
        test = ll2.pred[items] == ll2.true[items] and ll2.pred[items]=='hum'
        if test:
            tp+=1
            #fp = 0
    for items in range(len(ll2)):
        if ll2.true[items] == 'cam':
            test = ll2.pred[items] != ll2.true[items] 
            if test:
                fp+=1

    tn = 0
    for items in range(len(ll2)):
        test = ll2.pred[items] == ll2.true[items] and ll2.pred[items]=='cam'
        if test:
            tn+=1

    fn = 0
    for items in range(len(ll2)):
        if ll2.true[items] == 'hum':
            test = ll2.pred[items] != ll2.true[items] 
            if test:
                fn+=1
#precision

    if tp >0 or fp >0:
        prec = tp/(tp+fp)
    else:
        prec = []
        print('Only one class data in the validation file')
# recall
    if tp >0 or fn >0:
        rec = tp/(tp+fn)
        
    else:
        rec  = []
        print('Only one class data in the validation file')
#F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
    if prec or rec:
        f1 = 2*(prec*rec)/(prec+rec)
        
    else:
        f1 = []
        print('Only one class data in the validation file')

    return acc,prec,rec,f1,tp,tn,fp,fn


