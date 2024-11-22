def df_patient_connection(patient_data, conn_name):
    patient_conn = patient_data[patient_data['dest_type'] == conn_name] \
                    .drop(columns = 'dest_type')
    return patient_conn

def df_patient_features(patient_data, conn_names):
    patient_features = patient_data[~patient_data['dest_type'].isin(conn_names)] \
                        .rename(columns={'dest_id': 'feature_value', 'dest_type': 'feature_name'})
    patient_features = patient_features \
                        .pivot_table(index=['patient_id', 'source_label'], values='feature_value', aggfunc='first') \
                        .reset_index()
    return patient_features

def polish_patient_source(patient_data):
    patient_data['source_label'] = patient_data['source_label'].str.split('/').str[0]
    return patient_data

def standardize_patient_id(patient_data):
    for patient_id in patient_data['patient_id']:
        print(patient_id)
        print(patient_id.split('_')[1], patient_id.split('_')[2])
    #patient_data['patient_id'] = patient_data['patient_id'].apply(lambda x: f"<https://pubmed.ncbi.nlm.nih.gov/{x.split('_')[1]}?{x.split('_')[2]}>")
    return patient_data