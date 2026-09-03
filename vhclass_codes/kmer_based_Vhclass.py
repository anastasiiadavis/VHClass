"""
# © 2026. Triad National Security, LLC. All rights reserved.

"""
import joblib
import pandas as pd
from read_fast_to_df_publ import read_fasta_to_df_publ
import numpy as np
from encode_kmer_publ import encode_kmer_publ
from assess_perform_stats_publ import assess_perform_stats_publ
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("trained_model", type=str,
                    help="path to the joblib file with trained model")
parser.add_argument("k", type=int,
                    help="k in k-mer: how many amino acids to ecode kemrs with",default=3,choices=[2,3])
parser.add_argument("data_to_label", type=str,
                    help="fasta file with the data to be labelled (or validation set for testing)") 
parser.add_argument("save_predictions", type=str,
                    help="path to the file where to save predictions (.csv)") 
parser.add_argument("data_with_known_lbl", type=str,
                    help="True or False,True if using validation data with known labels")


args = parser.parse_args()
rf_loaded = joblib.load(args.trained_model)


data = args.data_to_label

seqs = read_fasta_to_df_publ(data)

feat_array = np.zeros((len(seqs), 20**args.k), dtype=int)

for items in range(len(seqs)):
    seq = seqs.sequence[items]
    for items2 in range(len(seq) - args.k + 1):
        kmer_tmp = seq[items2:items2+args.k]
        seq_to_num = encode_kmer_publ(kmer_tmp)
        feat_array[items, seq_to_num] += 1

feat_fixed = feat_array


predicted = rf_loaded.predict(feat_fixed)
predicted_labels=[]
predicted_labels = pd.concat([pd.DataFrame(predicted),seqs.header],axis = 1)
predicted_labels.reset_index(drop = True,inplace=True)
predicted_labels.columns = ['prediction','header']

predicted_labels.to_csv(args.save_predictions)



if args.data_with_known_lbl.lower() == "true":
    acc,prec,rec,f1,tp,tn,fp,fn = assess_perform_stats_publ(args.save_predictions)
    print(f'Accuracy = {acc}, Precision = {prec} , Recall = {rec}, F1 score = {f1}')
else:
    print('See predictions in a saved file')
    


 










