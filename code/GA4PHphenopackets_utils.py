import numpy as np
import pandas as pd

def df_patient_connection(patient_data, conn_name):
    patient_conn = patient_data[patient_data['dest_type'] == conn_name]
    return patient_conn[['patient_id', 'dest_id', 'dest_type']]

def df_patient_features(patient_data, conn_names):
    patient_features = patient_data[~patient_data['dest_type'].isin(conn_names)] \
                        .rename(columns={'dest_id': 'feature_value', 'dest_type': 'feature_name'})
    patient_features = patient_features[['patient_id', 'feature_name', 'feature_value']]
    patient_features = patient_features.pivot(index='patient_id', columns='feature_name', values='feature_value').reset_index()

    return patient_features

def standardize_patient_id(id):
    if id.startswith('PMID'):
        return f"<https://pubmed.ncbi.nlm.nih.gov/{id.split('_', 2)[1]}?{(id.split('_', 2)[2])}>"
    if id.startswith('STX'):
        return f"<https://pubmed.ncbi.nlm.nih.gov/35190816?{id.split('_', 1)[1]}>"
    return id

def standardize_sex_id(id):
    if id == 'FEMALE':
        return '<http://purl.obolibrary.org/obo/NCIT_C20197>'
    if id == 'MALE':
        return '<http://purl.obolibrary.org/obo/NCIT_C16576>'
    return id

def standardize_HP_id(id):    
    return f"<http://purl.obolibrary.org/obo/{id.replace(':','_')}>"

def standardize_disease_id(id):
    return f"<http://purl.obolibrary.org/obo/{id.replace(':','_')}>"

def get_patient_ids(patient_data):
    return patient_data['patient_id'].unique()

def get_article_id(patient_id):
    return patient_id.split('?')[0] + '>'

def create_patient_article_conns(patient_ids):
    article_conns = []
    for id in patient_ids:
        article_conns.append({
            'patient_id': id,
            'dest_id': get_article_id(id),
            'dest_type': 'article'
        })
    return pd.DataFrame(article_conns)

def create_patient_sex_conns(patient_sex_rows):
    print(len(patient_sex_rows))
    sex_conns = []
    for _,row in patient_sex_rows.iterrows():
        sex_conns.append({
            'patient_id': row['patient_id'],
            'dest_id': row['sex_id'],
            'dest_type': 'sex'
        })
    return pd.DataFrame(sex_conns)


    
    

