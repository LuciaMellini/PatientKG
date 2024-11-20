import pandas as pd
import numpy as np
from KG_utils import *
from settings import *

if __name__ == '__main__':
    nodes = pd.read_csv(data_path + 'nodesL.csv', low_memory=False)
    patient_conn = pd.read_csv(data_path + 'patient_connections.csv', low_memory=False)
    patient_conn
    patient_hpo = patient_conn[patient_conn['dest_id'].str.startswith('HP:')]
    patient_hpo = patient_hpo['dest_id']
    patient_hpo
    node_hpo = nodes[nodes['name'].str.contains("HP")]
    node_hpo = node_hpo['name'].apply(purl_to_id)
    
    not_in_arr2 = patient_hpo[~np.isin(patient_hpo, node_hpo)]
    print('Missing HPOs in knowledge graph:')
    print(not_in_arr2.unique())
    
    
    # for i in not_in_arr2[not_in_arr2=='HP:0030214'].index:
    #     patient_conn.loc[i, 'dest_id'] = 'HP:5200321'
    #     patient_conn.loc[i, 'dest_name'] = 'Amplification of sexual behavior'
    # for i in not_in_arr2[not_in_arr2=='HP:0002355'].index:
    #     patient_conn.loc[i, 'dest_id'] = 'HP:0001288'
    #     patient_conn.loc[i, 'dest_name'] = 'Gait disturbance'
    # for i in not_in_arr2[not_in_arr2=='HP:0006919'].index:
    #     patient_conn.loc[i, 'dest_id'] = 'HP:0000718'
    #     patient_conn.loc[i, 'dest_name'] = 'Aggressive behaviour'
    patient_conn.to_csv(data_path + 'patient_connections.csv', index=False)
