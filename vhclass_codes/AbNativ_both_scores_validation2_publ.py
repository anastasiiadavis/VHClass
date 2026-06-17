# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 13:54:56 2026

@author: 334992
"""

import pandas as pd
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("data_vh", type=str,
                    help="path to the VH AbNativ scores for given validation set")
parser.add_argument("data_vhh", type=str,
                    help="path to the VHH AbNativ scores for given validation set")

args = parser.parse_args()

all_vh = pd.read_csv(args.data_vh)
all_vhh = pd.read_csv(args.data_vhh)

comb_vh_vhh = []

for items in range(len(all_vh)):
    tmp = all_vh.seq_id[items]
    idx = list(all_vhh.seq_id).index(tmp)
    if tmp == all_vhh.seq_id[idx]:
        comb_vh_vhh.append([tmp,all_vhh.seq_id[idx],all_vh.vh_score[items],all_vhh.vhh_score[idx],all_vh.aligned_seq[items]])
    


comb_vh_vhh2 = []
comb_vh_vhh2 = pd.DataFrame(comb_vh_vhh, columns = ['id1','id2','vh_score','vhh_score','alignment'])
    


# now classify the sequences according to scores of both tools
true_hum=[]

true_cam=[]

for items in range(len(comb_vh_vhh2)):
    tmp = comb_vh_vhh2.id1[items][4:7]#comb_vh_vhh2.alignment[items][0] != '#' and
    if comb_vh_vhh2.vh_score[items]>0 and comb_vh_vhh2.vhh_score[items]>0:
        if tmp == 'hum':
            true_hum.append([comb_vh_vhh2.id1[items],comb_vh_vhh2.vh_score[items],comb_vh_vhh2.vhh_score[items],comb_vh_vhh2.alignment[items]])
        else:
            true_cam.append([comb_vh_vhh2.id1[items],comb_vh_vhh2.vh_score[items],comb_vh_vhh2.vhh_score[items],comb_vh_vhh2.alignment[items]])
        
    true_cam2 = pd.DataFrame(true_cam,columns =['tru_label','vh_score','vhh_score','alnm'])#

    true_hum2 = pd.DataFrame(true_hum,columns =['tru_label','vh_score','vhh_score','alnm'])#
#

plt.close('all')
plt.figure(1)

plt.scatter(true_cam2.vh_score,true_cam2.vhh_score)
plt.scatter(true_hum2.vh_score,true_hum2.vhh_score)

x1 = [0,1,2,3,4]  
y1 = [0,1,2,3,4]
plt.plot(x1,y1)

plt.ylim([0,1.1])
plt.xlim([0,1.1])

plt.title('VHH and VH scores of sequences from Validation Set 2')
plt.xlabel('AbNativ VH score')
plt.ylabel('AbNativ VHH score')
plt.legend(['Camelid sequences','Human Sequences'])
plt.rcParams.update({'font.size': 30})



mask = true_cam2.vhh_score>true_cam2.vh_score
correct = true_cam2[mask]


mask2 = true_hum2.vh_score>true_hum2.vhh_score
correct_h = true_hum2[mask2]


#Accuracy = (True Positives + True Negatives) / Total Predictions
acc = (len(correct_h)+len(correct))/(len(true_cam2)+len(true_hum2))
#precision

# fp = camelid sequence, classifieid as human
mask_fp = true_cam2.vhh_score<=true_cam2.vh_score
fp0 = true_cam2[mask_fp]
fp = len(fp0)
# fn = human sequence, classified as camelid
if (len(correct_h)+fp)>0:
    P =  len(correct_h)/(len(correct_h)+fp)  #prec = tp/(tp+fp)
else:
    P = []
    print('Precision not calculated: no human sequences were supplied in the validation data')
# recall

# fn = human sequences, classified as camelid ones
mask_fn = true_hum2.vhh_score>=true_hum2.vh_score
fn0 = true_hum2[mask_fn]
fn = len(fn0)
if fn >0:
#rec = tp/(tp+fn)
    R =len(correct_h)/(len(correct_h)+fn)
else:
    R = []
    print('Recall not calculated: no human sequences were supplied in the validation data')


#F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
if R:
    f1 = 2*(P*R)/(P+R)
else:
    f1=[]
    print('F1 score not calculated: no human sequences were supplied in the validation data')

#fp_data = pd.concat([fp0.alnm,fp0.vh_score,fp0.vhh_score],axis = 1)

print(f'Accuracy = {acc}, Precision = {P} , Recall = {R}, F1 score = {f1}')







