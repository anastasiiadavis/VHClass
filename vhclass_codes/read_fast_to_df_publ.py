# -*- coding: utf-8 -*-


import pandas as pd
from Bio import SeqIO

def read_fasta_to_df_publ(file_path):
    
    try:
        records = list(SeqIO.parse(file_path, "fasta"))
        data = {'header': [record.id for record in records],
                'sequence': [str(record.seq) for record in records]}
        df = pd.DataFrame(data,columns = ['header','sequence'])
        return df
    except Exception as e:
        print(f"Error reading FASTA file: {e}")
        return pd.DataFrame()