import pandas as pd
import subprocess
import numpy as np
import os

def replace_id_given_node_source(nodes, source, replace_function):
    nodes.loc[nodes['node_source'] == source, 'node_id'] = nodes.apply(replace_function, axis=1)
    return nodes

def assert_dtypes(df): 
    all_string = True
    for i, x in enumerate(df.dtypes.values): 
        if x != np.dtype('O'): 
            all_string = False
            print(df.columns[i], x)
    if not all_string: assert False
    
def hpo_ids(nodes):
    HPO_code = lambda x: "HP:" + str(x['node_id']).zfill(7)
    nodes = replace_id_given_node_source(nodes, 'HPO', HPO_code)
    return nodes
    
def omim_ids(nodes):
    mondo_path = './idUnification/'
    if not os.path.exists(mondo_path + 'mondo_references.csv'):
        subprocess.run(['bash', mondo_path + 'mondo_resource.sh'])

    df_omim_xref = pd.read_csv(mondo_path + 'mondo_references.csv', low_memory=False)
    df_omim_xref = df_omim_xref[df_omim_xref['ontology'].isin(['OMIM', 'OMIMPS'])]
    
    nodes['node_id'] = nodes['node_id'].astype(str)
    df_omim_xref['mondo_id'] = df_omim_xref['mondo_id'].astype(str)
    
    mondo_nodes = nodes[nodes['node_source']=='MONDO']
    omim_nodes = mondo_nodes.merge(df_omim_xref, left_on='node_id', right_on='mondo_id', how='inner')
    
    omim_nodes.loc[:, 'node_id'] = omim_nodes['ontology'] + ':' + omim_nodes['ontology_id'].astype(str)
    
    result = nodes.merge(omim_nodes[['node_idx', 'node_id']], on='node_idx', how='left', suffixes=('', '_y'))
    result.loc[result['node_source']=='MONDO', 'node_id'] = result.apply(lambda x: max(str(x['node_id']), str(x['node_id_y']), key=len), axis=1)
    
    return result.drop(columns=['node_id_y'])

    
    
    
    