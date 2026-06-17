from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
from read_fast_to_df_publ import read_fasta_to_df_publ
import numpy as np
from encode_kmer_publ import encode_kmer_publ


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("data", type=str,
                    help="path to the fasta file with training data")
parser.add_argument("k", type=int,
                    help="how many amino acids to ecode kmers with",default=3)
parser.add_argument("to_save", type=str,
                    help="path to where to store the trained model, .joblib")   
#"path/to_save.joblib"                 
# encode training data s k=mers with k = 3 #############################################
args = parser.parse_args()
seqs = read_fasta_to_df_publ(args.data)
#k = 3                                                                                                # make an argument for argparse, if more than 3, say that not supported

feat_array = np.zeros((len(seqs), 20**args.k), dtype=int)

for items in range(len(seqs)):
    seq = seqs.sequence[items]
    for items2 in range(len(seq) - args.k + 1):
        kmer_tmp = seq[items2:items2+args.k]
        seq_to_num = encode_kmer_publ(kmer_tmp)
        feat_array[items, seq_to_num] += 1

feat_fixed = feat_array

# train RF model######################################################

# get targets for trianing data only
data_with_lbl = read_fasta_to_df_publ(args.data)
target = []
for items in range(len(data_with_lbl)):
    target.append(data_with_lbl.header[items][0:5])          # target
target2 = pd.DataFrame(target, columns = ['target'])

# Random Forest implementation and save trained model

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(feat_fixed, np.array(target2).ravel())

joblib.dump(rf_classifier, args.to_save) 
    