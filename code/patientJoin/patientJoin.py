import pandas as pd
import argparse

import sys
sys.path.append('./../code')

from GA4PHphenopackets import *
from PrimeKG import *
from idUnification import *

def create_primekg_patient_nodes(patient_features):
    patient_nodes = []
    for idx, row in patient_features.iterrows():
        patient_nodes.append({
            'node_idx': idx,
            'node_id': row['patient_id'],
            'node_type': 'patient',
            'node_name': float('nan'),
            'node_source': row['source_label']
        })
    return pd.DataFrame(patient_nodes)
    
    
def create_primekg_patient_edges(kg_nodes, patient_data, merge_attribute):
    df_patient_conn = df_patient_connection(patient_data, merge_attribute)
    edge_index = df_patient_conn[['patient_idx', f'{merge_attribute}_id']].merge(kg_nodes[['node_idx', 'node_id', 'node_type']],  right_on='node_id', left_on=f'{merge_attribute}_id') \
                    .rename(columns={'node_idx': 'x_idx', 'patient_idx':'y_idx'}) \
                    .drop(columns=['node_id', f'{merge_attribute}_id'])
    patient_edges = []
    for _, row in edge_index.iterrows():
        patient_edges.append({
            'relation': f"patient_{row['node_type']}",
            'display_relation': f"has {row['node_type']}",
            'x_idx': row['x_idx'],
            'y_idx': row['y_idx']
        })
    return pd.DataFrame(patient_edges)

def append_patient_nodes_to_primekg(primekg_nodes, patient_nodes):
    primekg_with_patients_nodes = primekg_nodes._append(patient_nodes).reset_index().drop('index', axis=1)
    primekg_with_patients_nodes['node_idx'] = primekg_with_patients_nodes.index
    return primekg_with_patients_nodes

def append_patient_edges_to_primekg(primekg_edges, patient_edges):
    primekg_with_patients_edges = primekg_edges._append(patient_edges).reset_index().drop('index', axis=1)
    return primekg_with_patients_edges

def create_primekg_with_patients(primekg, patient_data, patient_connections):
    primekg_nodes = create_primekg_node_df(primekg)
    primekg_edges = create_primekg_edge_df(primekg, primekg_nodes)
    patient_features = df_patient_features(patient_data, patient_connections)
    
    print("\t Creating nodes...")
    patient_nodes = create_primekg_patient_nodes(patient_features)
    primekg_with_patients_nodes = append_patient_nodes_to_primekg(primekg_nodes, patient_nodes)
    
    print("\t Creating edges...")
    primekg_with_patients_edges = primekg_edges    
    for info_id in patient_connections:
        patient_info_edges = create_primekg_patient_edges(primekg_nodes, patient_data, info_id)
        primekg_with_patients_edges = append_patient_edges_to_primekg(primekg_with_patients_edges, patient_info_edges)
                                        
    return create_primekg(primekg_with_patients_nodes, primekg_with_patients_edges)
    
def parse_input():
    parser = argparse.ArgumentParser(description="Merge patient data with PrimeKG")
    
    parser.add_argument('primekg_path', type=str, help='Path to the PrimeKG CSV file')
    parser.add_argument('patient_data_path', type=str, help='Path to the patient data CSV file')
    
    # Optional output file argument
    parser.add_argument('-opkg', '--output_primekg', type=str, help='Path to save the output CSV file (optional)')
    parser.add_argument('-of', '--output_features', type=str, help='Path to save the output CSV file (optional)')
    
    args = parser.parse_args()
    primekg_path = args.primekg_path
    patient_data_path = args.patient_data_path
    output_primekg = args.output_primekg
    output_features = args.output_features
    
    return primekg_path, patient_data_path, output_primekg, output_features

if __name__ == "__main__":  
    primekg_path, patient_data_path, output_primekg, output_features = parse_input()
    
    print("Reading PrimeKG...") 
    primekg = pd.read_csv(primekg_path, low_memory=False)
    
    nodes = create_primekg_node_df(primekg)  
    nodes = hpo_ids(nodes)
    nodes = omim_ids(nodes)
        
    new_primekg = replace_nodes_in_kg(primekg, nodes)
    new_primekg.to_csv(primekg_path, index=False)
    
    print("Reading patient data...")
    patient_data = pd.read_csv(patient_data_path) \
                        .drop(columns=['source_type']).rename(columns={'source_id': 'patient_id'}) \
                        .rename(columns={'Unnamed: 0': 'patient_idx'})
                        

    patient_data = polish_patient_source(patient_data)
    
    patient_connections = ['HP', 'disease']
    
    print("Creating PrimeKG with patients...")
    primekg_with_patients = create_primekg_with_patients(primekg, patient_data, patient_connections)
    
    if output_primekg:
        primekg_with_patients.to_csv(output_primekg, index=False)
        print(f"Output saved to {output_primekg}")
        primekg_with_patients_nodes = create_primekg_node_df(primekg_with_patients).to_csv(output_primekg.replace('.csv', '_nodes.csv'), index=False)
        create_primekg_edge_df(primekg_with_patients, primekg_with_patients_nodes).to_csv(output_primekg.replace('.csv', '_edges.csv'), index=False)
    
   
    print("Creating patient features...")
    #patients not in patient_features only have edge connections in patient_data
    patient_features = df_patient_features(patient_data, patient_connections)
    
    if output_features:
        patient_features.to_csv(output_features, index=False)
        print(f"Output saved to {output_features}")