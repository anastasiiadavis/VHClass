

import pandas as pd
import numpy as np

def encode_kmer_publ(kmer):
    aa = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
          'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    values = {letter: index for index, letter in enumerate(aa)}

    kmer = kmer.upper()
    to_num = 0
    for i, residue in enumerate(kmer):
        to_num += values[residue] * (20 ** i)
    return to_num

    