import pandas as pd
from settings import *
from GA4PHphenopackets_utils import *

def create_nodes_from_ids(ids, node_type):
    new_nodes = []
    for id in ids:
        new_nodes.append({
            'name': id,
            'type': node_type
        })
    return pd.DataFrame(new_nodes)
    
def create_edges_from_connections(patient_conn, predicate_label):
    new_edges = []
    for _,row in patient_conn.iterrows():
        new_edges.append({
            'subject': row['patient_id'],
            'predicate': predicate_label,
            'object': row['dest_id']
        })
    return pd.DataFrame(new_edges)
    
    
def create_kg_with_patients(nodes, edges, patient_conn):
    # Create nodes
    patient_nodes = create_nodes_from_ids(get_patient_ids(patient_conn), 'Person')
    new_nodes = pd.concat([nodes, patient_nodes])

    # Create edges
    predicate_dict = {
        'Article': ('Part of', 'Has part'),
        'Sex': ('Subclassof', None),
        'Disease': ('Has disease', None),
        'HP': ('Has phenotype', 'Phenotype of')
    }
    
    new_edges = edges
    for conn_label, (direct_predicate, inverse_predicate) in predicate_dict.items():
        patient_conn_type = patient_conn[patient_conn['dest_type'] == conn_label]
        
        if direct_predicate:
            edges_from_conns = create_edges_from_connections(patient_conn_type, direct_predicate)
            new_edges = pd.concat([new_edges, edges_from_conns])
        
        if inverse_predicate:
            inverse_conns = patient_conn_type.rename(columns={'dest_id': 'patient_id', 'patient_id': 'dest_id'})
            edges_from_conns = create_edges_from_connections(inverse_conns, inverse_predicate)
            new_edges = pd.concat([new_edges, edges_from_conns])
            
    return new_nodes, new_edges

if __name__=='__main__':
        
    print("Reading KG...") 
    nodes = pd.read_csv(NODES_PREPARED_FILE, low_memory=False)
    edges = pd.read_csv(EDGES_PREPARED_FILE, low_memory=False)
    print("Reading patient data...")
    patient_conn = pd.read_csv(PATIENT_CONNECTIONS, low_memory=False)
    
    print("Merging KG with patients...")
    nodes_with_patients, edges_with_patients = create_kg_with_patients(nodes, edges, patient_conn)
        
    if SAVE_WITH_PATIENT_FILES:
        print(f"Saving output kg nodes to {NODES_WITH_PATIENT_FILE}")
        nodes_with_patients.to_csv(NODES_WITH_PATIENT_FILE, index=False)
        print(f"Saving output kg edges to {EDGES_WITH_PATIENT_FILE}")
        edges_with_patients.to_csv(EDGES_WITH_PATIENT_FILE, index=False)