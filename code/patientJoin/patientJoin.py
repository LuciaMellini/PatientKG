import os
import pandas as pd

import sys
sys.path.insert(0, '..')
from GA4PHphenopackets.GA4PHphenopackets import df_patient_hps, df_patient_disease, df_patient_features



def create_primekg_patient(patient_hps, patient_disease, patient_features, kg_nodes):
    patient_kg = pd.merge(patient_hps, kg_nodes, on='node_id', how='right')
    patient_kg = pd.merge(patient_disease, kg_nodes, on='node_id', how='right')
    return patient_kg

if __name__ == "__main__":
    data_path = '.'
    if not os.path.exists(data_path + '/primekg_nodes_with_ids.csv'):
        os.system('python3 id_unification.py')
        
    kg_nodes = pd.read_csv(data_path + '/primekg_nodes_with_ids.csv')
    patient_data = pd.read_csv(data_path + '/patients_GA4GHphenopacket.csv')
    patient_data = patient_data.drop(columns=['source_type', 'source_label']).rename(columns={'source_id': 'patient_id'})
    
    patient_hps = df_patient_hps(patient_data)
    patient_disease = df_patient_disease(patient_data)
    patient_features = df_patient_features(patient_data)
    print(patient_hps.head())
    print(patient_disease.head())