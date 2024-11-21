import pandas as pd
import numpy as np
from settings import *

if __name__ =="__main__":
    patient_conn = pd.read_csv(data_path + 'patient_connections.csv', low_memory=False)
    omim_mondo_map = pd.read_csv(data_path + 'omim_MONDO_MAP.txt', sep = '\t', low_memory=False, names = ['omim_id', 'mondo_id'])
    patient_omims = patient_conn[patient_conn['dest_id'].str.startswith('OMIM:')]
    omim_mondo_map = omim_mondo_map.apply(lambda x: x.str.replace('_', ':'))
    patient_omim_mapped = patient_omims.merge(omim_mondo_map, left_on='dest_id', right_on='omim_id') \
                    .drop(columns=['dest_id', 'omim_id']) \
                    .rename(columns={'mondo_id':'dest_id'})
                    
    patient_omim_mapped = patient_omim_mapped[patient_conn.columns]
    patient_other = patient_conn[~patient_conn['dest_id'].str.startswith('OMIM:')]
    
    patient_conn = pd.concat([patient_omim_mapped, patient_other])    
    patient_conn.to_csv(data_path + 'patient_connections.csv', index=False)
    
    
#patient_conn from 7165 to 71629 due to missing references from OMIM to MONDO