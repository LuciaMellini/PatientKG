import pandas as pd

def create_primekg_node_df(kg):
    nodes = pd.concat([kg.get(['x_id','x_type', 'x_name','x_source']).rename(columns={'x_id':'node_id', 'x_type':'node_type', 'x_name':'node_name','x_source':'node_source'}), 
                   kg.get(['y_id','y_type', 'y_name','y_source']).rename(columns={'y_id':'node_id', 'y_type':'node_type', 'y_name':'node_name','y_source':'node_source'})])
    nodes = nodes.drop_duplicates().reset_index().drop('index',axis=1).reset_index().rename(columns={'index':'node_idx'})
    return nodes

def create_primekg_edge_df(kg, nodes=None):
    if nodes is None:
        nodes = create_primekg_node_df(kg)
    edges = kg.merge(nodes, 'left', left_on=['x_id','x_type', 'x_name','x_source'], right_on=['node_id','node_type','node_name','node_source'])
    edges = edges.rename(columns={'node_idx':'x_idx'})
    edges = edges.merge(nodes, 'left', left_on=['y_id','y_type', 'y_name','y_source'], right_on=['node_id','node_type','node_name','node_source'])
    edges = edges.rename(columns={'node_idx':'y_idx'})
    edges = edges.get(['relation', 'display_relation','x_idx', 'y_idx'])
    return edges

def create_primekg_edge_index(edges):
    return edges.get(['x_idx', 'y_idx']).values

def create_primekg(nodes, edges):
    df_merged_x = edges.merge(nodes, left_on='x_idx', right_on='node_idx', suffixes=('', '_x')) \
                        .rename(columns={'node_id': 'x_id', 'node_type': 'x_type', 'node_name': 'x_name', 'node_source': 'x_source'})
    df_merged_final = pd.merge(df_merged_x, nodes, left_on='y_idx', right_on='node_idx', suffixes=('', '_y')) \
                        .rename(columns={'node_id': 'y_id', 'node_type': 'y_type', 'node_name': 'y_name', 'node_source': 'y_source'})

    return df_merged_final[['relation', 'display_relation', 'x_idx', 'x_id', 'x_type', 'x_name', 'x_source', 'y_idx', 'y_id', 'y_type', 'y_name', 'y_source']]
