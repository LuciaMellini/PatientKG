import pandas as pd
import argparse
from settings import *

def create_sex_nodes():    
    return pd.DataFrame({
        'name': ['<http://purl.obolibrary.org/obo/NCIT_C20197>', '<http://purl.obolibrary.org/obo/NCIT_C16576>'],
        'type': ['Person', 'Person']
    })
    
if __name__ == '__main__':
    
    nodes = pd.read_csv(NODES_RAW_FILE, low_memory=False)
    
    patient_conn = pd.read_csv(PATIENT_CONNECTIONS, low_memory=False)
    
    sex_nodes = create_sex_nodes()
    
    nodes = pd.concat([nodes, sex_nodes])
    
    article_nodes = patient_conn[patient_conn['dest_type'] == 'Article'].rename(columns={'dest_id': 'name', 'dest_type':'type'})[['name', 'type']].drop_duplicates()
    article_nodes['type'] = 'Article'
    
    nodes = pd.concat([nodes, article_nodes])
    
    if SAVE_PREPARED:
        print(f"Output saved to {NODES_PREPARED_FILE}")
        nodes.to_csv(NODES_PREPARED_FILE, index=False)
        print(f"Output saved to {EDGES_PREPARED_FILE}")
        nodes.to_csv(EDGES_PREPARED_FILE, index=False)
        