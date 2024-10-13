import pandas as pd
import subprocess
import numpy as np

def replace_id_given_node_source(nodes, source, replace_function):
    nodes.loc[nodes['node_source'] == source, 'node_id'] = nodes[nodes['node_source'] == source]['node_idx'].apply(replace_function)


def assert_dtypes(df): 
    all_string = True
    for i, x in enumerate(df.dtypes.values): 
        if x != np.dtype('O'): 
            all_string = False
            print(df.columns[i], x)
    if not all_string: assert False
    
def hpo_ids(nodes):
    HPO_code = lambda x: "HP:" + str(x).zfill(7)
    replace_id_given_node_source(nodes, 'HPO', HPO_code)
    
def omim_ids(nodes):
    subprocess.run(['bash', 'mondo_resource.sh'])
    
    df_mondo_xref = pd.read_csv(data_path+'/mondo_references.csv', low_memory=False)
    df_omim_xref = df_mondo_xref[df_mondo_xref['ontology'].isin(['OMIM', 'OMIMPS'])]
    
    df_mondo_with_ontology = df_omim_xref.merge(nodes[nodes['node_source']=='MONDO'], left_on='mondo_id', right_on='node_idx')
    
    OMIM_code = lambda x: {f"{df_mondo_with_ontology['ontology'].loc('node_idx'==x)}:{df_mondo_with_ontology['ontology_id'].loc('node_idx'==x)}"}
    replace_id_given_node_source(df_mondo_with_ontology, 'MONDO', OMIM_code)
    
    nodes = df_mondo_with_ontology.drop(['ontology', 'ontology_id'], axis=1)
    
    


if __name__ == '__main__':
    data_path = "."
    primekg = pd.read_csv('../PrimeKG.csv', low_memory=False)
    nodes = pd.concat([primekg.get(['x_id','x_type', 'x_name','x_source']).rename(columns={'x_id':'node_id', 'x_type':'node_type', 'x_name':'node_name','x_source':'node_source'}), 
                   primekg.get(['y_id','y_type', 'y_name','y_source']).rename(columns={'y_id':'node_id', 'y_type':'node_type', 'y_name':'node_name','y_source':'node_source'})])
    nodes = nodes.drop_duplicates().reset_index().drop('index',axis=1).reset_index().rename(columns={'index':'node_idx'})
    
    hpo_ids(nodes)
    print(nodes[nodes['node_source'] == 'HPO'].head())
    
    omim_ids(nodes)
    print(nodes[nodes['node_source'] == 'MONDO'].head(100))
    
        
    
    # print(nodes[nodes['node_source'] == 'HPO'].head())
    # print(nodes[nodes['node_source'] == 'MONDO'].head())