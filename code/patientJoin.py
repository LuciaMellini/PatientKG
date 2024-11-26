import argparse
import pandas as pd
from KG_utils import *
from GA4PHphenopackets_utils import *

def parse_input():
    parser = argparse.ArgumentParser(description="Merge patient data with PrimeKG")
    
    parser.add_argument('node_path', type=str, help='Path to the KG node CSV file')
    parser.add_argument('edge_path', type=str, help='Path to the KG edge CSV file')
    parser.add_argument('patient_data_path', type=str, help='Path to the patient connection data CSV file')
    
    parser.add_argument('-okgn', '--output_kg_nodes', type=str, help='Path to save the output kg nodes CSV file (optional)')
    parser.add_argument('-okge', '--output_kg_edges', type=str, help='Path to save the output kg edges CSV file (optional)')

    
    args = parser.parse_args()
    node_path = args.node_path
    edge_path = args.edge_path
    patient_data_path = args.patient_data_path
    output_kg_nodes = args.output_kg_nodes
    output_kg_edges = args.output_kg_edges
    
    return node_path, edge_path, patient_data_path, output_kg_nodes, output_kg_edges

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
        'article': ('Part of', 'Has part'),
        'sex': ('Subclassof', None),
        'disease': ('Has disease', None),
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

    node_path, edge_path, patient_conn, output_kg_nodes, output_kg_edges = parse_input()
        
    print("Reading KG...") 
    nodes = pd.read_csv(node_path, low_memory=False)
    edges = pd.read_csv(edge_path, low_memory=False)
    print("Reading patient data...")
    patient_conn = pd.read_csv(patient_conn, low_memory=False)
    
    print("Merging KG with patients...")
    nodes_with_patients, edges_with_patients = create_kg_with_patients(nodes, edges, patient_conn)
        
    if output_kg_nodes:
        print(f"Saving output kg nodes to {output_kg_nodes}")
        nodes_with_patients.to_csv(output_kg_nodes, index=False)
    if output_kg_edges:
        print(f"Saving output kg edges to {output_kg_edges}")
        edges_with_patients.to_csv(output_kg_edges, index=False)