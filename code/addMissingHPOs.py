import pandas as pd
import numpy as np
from KG_utils import *
from settings import *

if __name__ == '__main__':
    nodes = pd.read_csv(data_path + 'nodesL.csv', low_memory=False)
    patient_conn = pd.read_csv(data_path + 'patient_connections.csv', low_memory=False)
    
    patient_hpo = patient_conn[patient_conn['dest_type']=='HP']['dest_id'].unique()
    node_hpo = nodes[nodes['name'].str.contains("HP")]['name']
    
    not_in_node_hpo = patient_hpo[~np.isin(patient_hpo, node_hpo)]
    for hpo in not_in_node_hpo:
        print(f"Adding {hpo}")
    # print('Missing HPOs in knowledge graph:')
    # print(not_in_node_hpo.unique())
    
    
    for i in patient_conn[patient_conn['dest_id']=='<http://purl.obolibrary.org/obo/HP_0030214>'].index:
        patient_conn.loc[i, 'dest_id'] = 'HP:5200321'
        patient_conn.loc[i, 'dest_label'] = 'Amplification of sexual behavior'
    for i in patient_conn[patient_conn['dest_id']=='<http://purl.obolibrary.org/obo/HP_0002355>'].index:
        patient_conn.loc[i, 'dest_id'] = 'HP:0001288'
        patient_conn.loc[i, 'dest_label'] = 'Gait disturbance'
    for i in patient_conn[patient_conn['dest_id']=='Adding <http://purl.obolibrary.org/obo/HP_0006919>'].index:
        patient_conn.loc[i, 'dest_id'] = 'HP:0000718'
        patient_conn.loc[i, 'dest_label'] = 'Aggressive behaviour'
        
    patient_conn.to_csv(data_path + 'patient_connections.csv', index=False)
