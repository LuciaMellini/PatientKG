import pandas as pd
from settings import *
from GA4PHphenopackets_utils import *

def standardize_ids(patient_data, id_type, standardize_func):
    patient_data.loc[patient_data['dest_type'] == id_type, 'dest_id'] = patient_data.loc[patient_data['dest_type'] == id_type, 'dest_id'].apply(standardize_func)
    return patient_data

def standardize_patient_ids(patient_data):
    patient_data['patient_id'] = patient_data['patient_id'].apply(standardize_patient_id)
    return patient_data

def omim_to_mondo_ids(patient_data):
    omim_mondo_map = pd.read_csv(OMIM_MONDO_MAP, sep = '\t', low_memory=False, names = ['omim_id', 'mondo_id'])
    omim_mondo_map = omim_mondo_map.apply(lambda x: x.str.replace('_', ':'))
    omim_mondo_dict = dict(zip(omim_mondo_map['omim_id'], omim_mondo_map['mondo_id']))
    patient_data['dest_id'] = patient_data['dest_id'].apply(lambda x: omim_mondo_dict[x] if x in omim_mondo_dict else x)
    patient_data = patient_data[~patient_data['dest_id'].str.startswith('OMIM:')]
    return patient_data

def remove_patients_without_disease_connection(patient_conn):
    patients_with_disease_conns = patient_conn[patient_conn['dest_type'] == 'disease']['patient_id'].unique()
    patients_without_disease_conns = patient_conn[~patient_conn['patient_id'].isin(patients_with_disease_conns)]['patient_id'].unique()
    print(len(patients_without_disease_conns))
    for patient in patients_without_disease_conns:
        print(f"Removed patient {patient} without disease connection")
    return patient_conn[patient_conn['patient_id'].isin(patients_with_disease_conns)]

if __name__ == "__main__":      
   
    patient_data = pd.read_csv(PATIENT_PATH) \
                        .drop(columns=['source_type', 'Unnamed: 0']).rename(columns={'source_id': 'patient_id'})  
                 
    print("Standardizing IDs in patient data")
    patient_data = omim_to_mondo_ids(patient_data)
    
    patient_data = standardize_patient_ids(patient_data)
    
    standardization_funcs = [standardize_sex_id, standardize_HP_id, standardize_disease_id]    
    for func in standardization_funcs:
        patient_data = standardize_ids(patient_data, func.__name__.split('_')[1], func)
   
    
    patient_ids = get_patient_ids(patient_data)
    patient_article_conns = create_patient_article_conns(patient_ids)
    patient_data = pd.concat([patient_data, patient_article_conns])
    
    print("Creating patient connections") 
    conns = ['HP', 'disease', 'sex', 'article']
    patient_conn = pd.DataFrame()
    for conn in conns:
        patient_conn = pd.concat([df_patient_connection(patient_data, conn), patient_conn], ignore_index=True)
        
    print("Removing patients without disease connection")  
    patient_conn =remove_patients_without_disease_connection(patient_conn)
    
    if SAVE_PATIENT_CONNECTIONS:        
        patient_conn.to_csv(PATIENT_CONNECTIONS, index = False)
        print(f"Output saved to {PATIENT_CONNECTIONS}")
        
     
    print("Creating patient features...")
    patient_features = df_patient_features(patient_data, conns)
    
    if SAVE_PATIENT_FEATURES:
        patient_features.to_csv(PATIENT_FEATURES, index=False)
        print(f"Output saved to {PATIENT_FEATURES}")
    
    