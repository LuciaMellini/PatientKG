import pandas as pd
import numpy as np
from settings import *

if __name__ == '__main__':
    nodes = pd.read_csv(NODES_PREPARED_FILE, low_memory=False)
    patient_conn = pd.read_csv(PATIENT_CONNECTIONS, low_memory=False)
    
    patient_hpo = patient_conn[patient_conn['dest_type']=='HP']['dest_id'].unique()
    node_hpo = nodes[nodes['name'].str.contains("HP")]['name']
    
    not_in_node_hpo = patient_hpo[~np.isin(patient_hpo, node_hpo)]
    for hpo in not_in_node_hpo:
        print(f"Adding {hpo}")
    # print('Missing HPOs in knowledge graph:')
    # print(not_in_node_hpo.unique())
   
    hpo_mapping = HPO_MAP_NOT_IN_KG
    for key, value in hpo_mapping.items():
        indices = patient_conn[patient_conn['dest_id'] == key].index
        patient_conn.loc[indices, 'dest_id'] = value["HPO_id"]
        patient_conn.loc[indices, 'dest_label'] = value["label"]
        
    if SAVE_PATIENT_CONNECTIONS:
        patient_conn.to_csv(PATIENT_CONNECTIONS, index=False)
