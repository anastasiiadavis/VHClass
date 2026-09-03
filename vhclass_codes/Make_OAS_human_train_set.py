"""
# © 2026. Triad National Security, LLC. All rights reserved.

"""

# Need to get 480 human sequences from OAS databse for training set
# 
import pandas as pd
import numpy as np
import re
from matplotlib import pyplot as plt
from read_fast_to_df import read_fasta_to_df
from numpy import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("human_data1", type=str,
                    help="path to the dataset used as human training data")
parser.add_argument("human_data2", type=str,
                    help="path to the dataset used as human training data")
parser.add_argument("human_data3", type=str,
                    help="path to the dataset used as human training data")
parser.add_argument("human_data4", type=str,
                    help="path to the dataset used as human training data")
parser.add_argument("human_data5", type=str,
                    help="path to the dataset used as human training data")
parser.add_argument("human_data6", type=str,
                    help="path to the dataset used as human training data")
parser.add_argument("human_data7", type=str,
                    help="path to the dataset used as human training data")

parser.add_argument("save_to_fasta", type=str,
                    help="path to location of where to save the human training superset")

args = parser.parse_args()
df_h1 = pd.read_csv(args.human_data1, header = 1, usecols = 'sequence_alignment_aa') 
df_h2 = pd.read_csv(args.human_data2, header = 1, usecols = 'sequence_alignment_aa')
df_h3 = pd.read_csv(args.human_data3, header = 1, usecols = 'sequence_alignment_aa')
df_h4 = pd.read_csv(args.human_data4, header = 1, usecols = 'sequence_alignment_aa')
df_h5 = pd.read_csv(args.human_data5, header = 1, usecols = 'sequence_alignment_aa')
df_h6 = pd.read_csv(args.human_data6, header = 1, usecols = 'sequence_alignment_aa')
df_h7 = pd.read_csv(args.human_data7, header = 1, usecols = 'sequence_alignment_aa')

# concatenate full sequences 
df_fin_vh = []
df_fin_vh = pd.concat([df_h1.sequence_alignment_aa,df_h2.sequence_alignment_aa,df_h3.sequence_alignment_aa,df_h4.sequence_alignment_aa,df_h5.sequence_alignment_aa,df_h6.sequence_alignment_aa,df_h7.sequence_alignment_aa],axis = 0)
df_shuffled = df_fin_vh.sample(frac=1, random_state=42).reset_index(drop=True)#
df_shuffled.drop_duplicates(inplace = True, ignore_index = True)

ll = []
for items in range(len(df_shuffled)):
    ll.append(len(df_shuffled[items]))
    
len_filtered_vh = []
for items in range(len(df_shuffled)):
    if len(df_shuffled[items])>=100:
        len_filtered_vh.append(df_shuffled[items])
len_filtered_vh_2 = pd.DataFrame(len_filtered_vh, columns = ['sequence'])


# fasta

fn_to_blast =args.save_to_fasta
fileOutput = open(fn_to_blast, "w")
counter = 0
for items in range(len(len_filtered_vh_2)):
    counter+=1
    fileOutput.write(">human"+str(counter) + "\n")
    fileOutput.write(len_filtered_vh_2.sequence[items] + "\n")
    #print(counter)
    
fileOutput.close()






















