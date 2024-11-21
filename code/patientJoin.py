import argparse
import pandas as pd
from KG_utils import *

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

def create_patient_nodes(patient_conn):
    patient_nodes = []
    for id in patient_conn['patient_id'].unique():
        patient_nodes.append({
            'name': id,
            'type': 'Patient'
        })
    return pd.DataFrame(patient_nodes)

def create_patient_edges(patient_conn, nodes):
    nodes = nodes.copy()
    nodes['name_copy'] =  nodes['name']
    nodes['name'] = nodes['name'].apply(purl_to_id)
    edges_new = nodes.merge(patient_conn[['patient_id', 'dest_id']], left_on = 'name', right_on = 'dest_id', how='right') \
                .drop(columns = ['type', 'dest_id'])   \
                .rename(columns = {'name': 'object', 'patient_id': 'subject'}) 
   
    edges_new.loc[edges_new['object'].str.contains('HP'), 'predicate'] = 'Has phenotype'
    edges_new.loc[edges_new['object'].str.contains('MONDO'), 'predicate'] = 'Has disease'
    edges_new['object'] = edges_new['name_copy']
    edges_new = edges_new.drop(columns = ['name_copy'])    

    return edges_new
    
def create_kg_with_patients(nodes, edges, patient_conn):
    patient_nodes = create_patient_nodes(patient_conn)
    new_nodes = pd.concat([nodes, patient_nodes])

    patient_edges = create_patient_edges(patient_conn, new_nodes)
    new_edges = pd.concat([edges, patient_edges])
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