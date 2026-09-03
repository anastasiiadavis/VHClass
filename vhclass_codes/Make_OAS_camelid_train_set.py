"""
# © 2026. Triad National Security, LLC. All rights reserved.

"""
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("camelid_data", type=str,
                    help="path to the dataset used as camelid training data")
parser.add_argument("save_to_fasta", type=str,
                    help="path to location of where to save the camelid training superset")

args = parser.parse_args()

df_c1 = pd.read_csv(args.camelid_data, header = 1, usecols = ['sequence_alignment_aa'])

# Shuffle DataFrame rows 
df_shuffled = df_c1.sample(frac=0.062, random_state=100).reset_index(drop=True)# take 20K sequences
df_shuffled.drop_duplicates(inplace = True,ignore_index = True)

ll = []
for items in range(len(df_shuffled)):
    ll.append(len(df_shuffled.sequence_alignment_aa[items]))
    
len_filtered_vh = []
for items in range(len(df_shuffled)):
    if len(df_shuffled.sequence_alignment_aa[items])>=100:
        len_filtered_vh.append(df_shuffled.sequence_alignment_aa[items])
len_filtered_vh_2 = pd.DataFrame(len_filtered_vh, columns = ['sequence'])


# fasta

fn_to_blast =args.save_to_fasta

fileOutput = open(fn_to_blast, "w")
counter = 0
for items in range(len(len_filtered_vh_2)):
    counter+=1
    fileOutput.write(">camelid"+str(counter) + "\n")
    fileOutput.write(len_filtered_vh_2.sequence[items] + "\n")
    #print(counter)
    
fileOutput.close()























