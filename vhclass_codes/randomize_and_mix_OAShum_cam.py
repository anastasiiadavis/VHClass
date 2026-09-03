"""
# © 2026. Triad National Security, LLC. All rights reserved.

"""

import pandas as pd
import numpy as np
import re
from matplotlib import pyplot as plt
from read_fast_to_df_publ import read_fasta_to_df_publ
from numpy import random
import argparse
parser = argparse.ArgumentParser()
# load the separately curated human and camelid supersets 

parser.add_argument("cam_data", type=str,
                    help="path to the filtered fasta file with camelid training data")
parser.add_argument("hum_data", type=str,
                    help="path to the filtered fasta file with human training data")
parser.add_argument("save_to_fasta", type=str,
                    help="where to save the final trianing set in fasta format")

args = parser.parse_args()

cam_labeled = read_fasta_to_df_publ(args.cam_data)
human_labeled = read_fasta_to_df_publ(args.hum_data)

# to make different sizes of trainset, take different fraction of the superset
# take 53% of he camelid set, for the 20K combined set
df_c2 = cam_labeled.sample(frac=0.53, random_state=30).reset_index(drop=True)#drop=True
# take 50% of he human set, so both human and camelid are at 10K

df_h2 = human_labeled.sample(frac=0.5, random_state=30).reset_index(drop=True)#drop=True

# concatenate the two data frames and randomly shuffle
df_combined = []
df_combined = pd.concat([df_h2,df_c2],axis = 0,ignore_index = True)
#Shuffle DataFrame rows
df_shuffled = df_combined.sample(frac=1, random_state=30).reset_index(drop=True)#drop=True

# save the randomized data in fasta format for training set

fn_to_blast =args.save_to_fasta
fileOutput = open(fn_to_blast, "w")
counter = 0
for items in range(len(df_shuffled)):
    counter+=1
    fileOutput.write(">"+str(df_shuffled.header[items]) + "\n")
    fileOutput.write(df_shuffled.sequence[items] + "\n")
    #print(counter)
    
fileOutput.close()