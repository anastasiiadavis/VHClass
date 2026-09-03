"""
# © 2026. Triad National Security, LLC. All rights reserved.

"""

import pandas as pd
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
if len(correct_h) == 0:
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

print(f'Accuracy = {acc}, Precision = {P} , Recall = {R}, F1 score = {f1}')







