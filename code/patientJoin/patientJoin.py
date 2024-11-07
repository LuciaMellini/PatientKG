import pandas as pd
import argparse
from idUnification import *
import sys
sys.path.append('..')
from PrimeKG_utils import *
from GA4PHphenopackets_utils import *

def create_primekg_patient_nodes(patient_id_source):
    patient_nodes = []
    for _, row in patient_id_source.iterrows():
        patient_nodes.append({
            'node_idx': row['patient_idx'],
            'node_id': row['patient_idx'],
            'node_type': 'patient',
            'node_name': row['patient_id'],
            'node_source': row['source_label']
        })
    return pd.DataFrame(patient_nodes)
    
def create_primekg_patient_edges(kg_nodes, patient_data, merge_attribute):
    df_patient_conn = df_patient_connection(patient_data, merge_attribute)
    patients = kg_nodes[kg_nodes['node_type']=='patient']
    edge_index = df_patient_conn[['patient_idx', f'{merge_attribute}_id']] \
                .merge(patients[['node_name', 'node_id']], right_on='node_id', left_on='patient_idx') \
                .drop(columns = ['patient_idx']) \
                .rename(columns={'node_id':'patient_idx'}) \
                .merge(kg_nodes[['node_idx', 'node_id', 'node_type']],  right_on='node_id', left_on=f'{merge_attribute}_id') \
                .rename(columns={'node_idx': 'x_idx', 'patient_idx':'y_idx'}) \
                .drop(columns=[f'{merge_attribute}_id'])
    del df_patient_conn
    patient_edges = []
    for _, row in edge_index.iterrows():
        patient_edges.append({
            'relation': f"patient_{row['node_type']}",
            'display_relation': f"has {row['node_type']}",
            'x_idx': row['x_idx'],
            'y_idx': row['y_idx']
        })
        
    return pd.DataFrame(patient_edges)

def create_primekg_with_patients(primekg, patient_data, patient_connections):
    primekg_nodes = create_primekg_node_df(primekg)
    primekg_edges = create_primekg_edge_df(primekg)
    
    print("\t Creating nodes...")
    patient_nodes = create_primekg_patient_nodes(patient_data[['source_label', 'patient_id', 'patient_idx']].drop_duplicates())
    primekg_with_patients_nodes = pd.concat([primekg_nodes, patient_nodes], ignore_index=True)
    primekg_with_patients_nodes['node_idx'] = primekg_with_patients_nodes.index
    # del primekg_nodes, patient_nodes
    print("\t Creating edges...")
    patient_edges = pd.DataFrame()
    for info_id in patient_connections:
        patient_edges = pd.concat([patient_edges, create_primekg_patient_edges(primekg_with_patients_nodes, patient_data, info_id)], ignore_index=True)
    # primekg_with_patients_edges = pd.concat([primekg_edges, patient_edges], ignore_index=True)
    
    # del primekg_edges, patient_edges    
    
    primekg_with_patients = create_primekg(primekg_with_patients_nodes, patient_edges)
    return pd.concat([primekg, primekg_with_patients], ignore_index=True)
    
def parse_input():
    parser = argparse.ArgumentParser(description="Merge patient data with PrimeKG")
    
    parser.add_argument('primekg_path', type=str, help='Path to the PrimeKG CSV file')
    parser.add_argument('patient_data_path', type=str, help='Path to the patient data CSV file')
    
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
    nodes.to_csv('nodes.csv')

    primekg = replace_nodes_in_kg(primekg, nodes)
    primekg.to_csv(primekg_path, index=False)
    # create_primekg_node_df(primekg).to_csv(primekg_path.replace('.csv', '_nodes.csv'), index=False)
    # create_primekg_edge_df(primekg, nodes).to_csv(primekg_path.replace('.csv', '_edges.csv'), index=False)
    
    print("Reading patient data...")
    patient_data = pd.read_csv(patient_data_path) \
                        .drop(columns=['source_type', 'Unnamed: 0']).rename(columns={'source_id': 'patient_id'}) 
    patient_data['patient_idx'] = pd.factorize(patient_data['patient_id'])[0]                       

    patient_data = polish_patient_source(patient_data)
    
    patient_connections = ['HP', 'disease']
    
    print("Creating PrimeKG with patients...")
    primekg_with_patients = create_primekg_with_patients(primekg, patient_data, patient_connections)
      
    if output_primekg:
        primekg_with_patients.to_csv(output_primekg, index=False)
        print(f"Output saved to {output_primekg}")
        # create_primekg_node_df(primekg_with_patients).to_csv(output_primekg.replace('.csv', '_nodes.csv'), index=False)
        # create_primekg_edge_df(primekg_with_patients, primekg_with_patients_nodes).to_csv(output_primekg.replace('.csv', '_edges.csv'), index=False)
    del primekg_with_patients
   
    print("Creating patient features...")
    #patients not in patient_features only have edge connections in patient_data
    patient_features = df_patient_features(patient_data, patient_connections)
    
    if output_features:
        patient_features.to_csv(output_features, index=False)
        print(f"Output saved to {output_features}")