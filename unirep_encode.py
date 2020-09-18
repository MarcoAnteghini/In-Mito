#!/usr/bin/env python

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import numpy as np
from Bio import SeqIO

tf.set_random_seed(42)
np.random.seed(42)


#if USE_FULL_1900_DIM_MODEL:
    # Sync relevant weight files
#    !aws s3 sync --no-sign-request --quiet s3://unirep-public/1900_weights/ 1900_weights/

    # Import the mLSTM babbler model
from unirep import babbler1900 as babbler

    # Where model weights are stored.
MODEL_WEIGHT_PATH = "."

#else:
    # Sync relevant weight files
#    !aws s3 sync --no-sign-request --quiet s3://unirep-public/64_weights/ 64_weights/

    # Import the mLSTM babbler model
#from unirep import babbler64 as babbler

    # Where model weights are stored.
#    MODEL_WEIGHT_PATH = "./64_weights"


b = babbler('1900_weights')





try:
    filename=sys.argv[1]
except:
    print('YOU HAVE TO INPUT A FASTA FILE','\n','Usage: ./unirep_encode.py file.fasta')

d={}
with open(filename) as fasta:
    for record in SeqIO.parse(fasta, "fasta"):
        try:
            sequence=record.seq
            ids=record.id
            d[ids.split('|')[1]] = sequence
           # print(sequence)
        except:
            print('Something wrong')
            pass


c=0
to_check=[]
for keys in d:
    try:
        ur = b.get_rep(d[keys])
        tosave1 = np.asarray(ur[0])
#        tosave2 = np.asarray(ur[1])
#        tosave3 = np.asarray(ur[2])

        np.save(keys+'_UniRep1', tosave1)
#        np.save(ids.split('|')[1]+'_UniRep2', tosave2)
#        np.save(ids.split('|')[1]+'_UniRep3', tosave3)
        c=c+1
        print('ID:',keys,' '*20,c,'/',len(d))
    except:
        to_check.append(keys)
        pass
print(to_check)
