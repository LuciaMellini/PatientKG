import pandas as pd
import subprocess
import numpy as np
import os
import sys
sys.path.append('../..')
from utils import *

def replace_id_given_node_source(nodes, source, replace_function):
    nodes.loc[nodes['node_source'] == source, 'node_id'] = nodes.apply(replace_function, axis=1)

def assert_dtypes(df): 
    all_string = True
    for i, x in enumerate(df.dtypes.values): 
        if x != np.dtype('O'): 
            all_string = False
            print(df.columns[i], x)
    if not all_string: assert False
    
def hpo_ids(nodes):
    nodes_updated = nodes.copy()
    HPO_code = lambda x: "HP:" + str(x['node_id']).zfill(7)
    replace_id_given_node_source(nodes_updated, 'HPO', HPO_code)
    return nodes_updated
    
def omim_ids(nodes):
    subprocess.run(['bash', 'mondo_resource.sh'])
    
    df_mondo_xref = pd.read_csv(data_path+'/mondo_references.csv', low_memory=False)
    df_omim_xref = df_mondo_xref[df_mondo_xref['ontology'].isin(['OMIM', 'OMIMPS'])]
    print(len(df_omim_xref))
    
    nodes['node_id'] = nodes['node_id'].astype(str)
    df_omim_xref['mondo_id'] = df_omim_xref['mondo_id'].astype(str)
    
    nodes_mondo = nodes[nodes['node_source']=='MONDO']
    df_omim_with_ontology = pd.merge(nodes_mondo, df_omim_xref, left_on='node_id', right_on='mondo_id', how='inner')
    
    OMIM_code = lambda x: str(x['ontology']) + ":" + str(x['ontology_id'])
    replace_id_given_node_source(df_omim_with_ontology, 'MONDO', OMIM_code)
    
    df_omim_with_ontology = df_omim_with_ontology.drop(columns = ['ontology', 'ontology_id', 'mondo_id'])
    
    nodes_updated = pd.merge(nodes, df_omim_with_ontology, on='node_idx', how='left', suffixes=('', '_y'))
    keep_ontology = lambda x: max(str(x['node_id']), str(x['node_id_y']), key=len)
    replace_id_given_node_source(nodes_updated, 'MONDO', keep_ontology)
    columns_to_drop = [col for col in nodes_updated.columns if col.endswith('_y')]
    nodes_updated = nodes_updated.drop(columns=columns_to_drop)   
    return nodes_updated

def replace_nodes_in_kg(kg, nodes):
    new_primekg = kg.copy()
    
    new_primekg = new_primekg.drop(columns=['x_id','y_id'])
    new_primekg = pd.merge(new_primekg, nodes[['node_idx', 'node_id']], left_on='x_index', right_on='node_idx', how='left')
    new_primekg = pd.merge(new_primekg, nodes[['node_idx', 'node_id']], left_on='y_index', right_on='node_idx', how='left')
    
    return new_primekg
    
    

    
if __name__ == '__main__':
    data_path = "."
    primekg_file = './../../PrimeKG.csv'
    primekg = pd.read_csv(primekg_file, low_memory=False)
    
    if not os.path.exists(data_path + '/nodes_with_ids.csv'):
        nodes = create_node_df(primekg)  
        nodes = hpo_ids(nodes)
        nodes = omim_ids(nodes)
        
    else:
        nodes = pd.read_csv(data_path + '/nodes_with_ids.csv')
        
    print(primekg.head())
    new_primekg = replace_nodes_in_kg(primekg, nodes)
    new_primekg.to_csv(primekg_file, index=False)
    
    