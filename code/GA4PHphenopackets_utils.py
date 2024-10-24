def df_patient_connection(patient_data, conn_name):
    patient_hps = patient_data[patient_data['dest_type'] == conn_name] \
                    .drop(columns = 'dest_type') \
                    .rename(columns={'dest_id': f'{conn_name}_id', 'dest_label': f'{conn_name}_name'})
    return patient_hps

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