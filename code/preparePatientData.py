import pandas as pd
import argparse
import sys
sys.path.append('..')
from GA4PHphenopackets_utils import *


def parse_input():
    parser = argparse.ArgumentParser(description="Merge patient data with PrimeKG")
    
    parser.add_argument('patient_data_path', type=str, help='Path to the patient data CSV file')
    
    parser.add_argument('-oc', '--output_conn', type=str, help='Path to save the output CSV file (optional)')
    parser.add_argument('-of', '--output_features', type=str, help='Path to save the output CSV file (optional)')
    
    args = parser.parse_args()
    patient_data_path = args.patient_data_path
    output_connections = args.output_conn
    output_features = args.output_features
    
    return patient_data_path, output_connections, output_features


    
if __name__ == "__main__":      
    patient_data_path, output_connections, output_features = parse_input()    
    
    print("Reading and manipulating patient data...")
    patient_data = pd.read_csv(patient_data_path) \
                        .drop(columns=['source_type', 'Unnamed: 0']).rename(columns={'source_id': 'patient_id'})                     
    
    print(patient_data.head())
    patient_data = standardize_patient_id(patient_data)
    patient_data = polish_patient_source(patient_data)
    
    print("Creating patient connections...") 
    conns = ['HP', 'disease']
    patient_conn = pd.DataFrame()
    for conn in conns:
        patient_conn = pd.concat([df_patient_connection(patient_data, conn), patient_conn], ignore_index=True)
        
    if output_connections:        
        patient_conn.to_csv(output_connections, index = False)
        print(f"Output saved to {output_connections}")
        
        
    print("Creating patient features...")
    patient_features = df_patient_features(patient_data, conns)
    
    if output_features:
        patient_features.to_csv(output_features, index=False)
        print(f"Output saved to {output_features}")
    
    