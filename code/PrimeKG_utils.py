import pandas as pd

def create_primekg_node_df(kg):
    nodes = pd.concat([kg.get(['x_id','x_type', 'x_name','x_source']).rename(columns={'x_id':'node_id', 'x_type':'node_type', 'x_name':'node_name','x_source':'node_source'}), 
                   kg.get(['y_id','y_type', 'y_name','y_source']).rename(columns={'y_id':'node_id', 'y_type':'node_type', 'y_name':'node_name','y_source':'node_source'})])
    nodes = nodes.drop_duplicates().reset_index().drop('index',axis=1).reset_index().rename(columns={'index':'node_idx'})
    return nodes

def create_primekg_edge_df(kg):
    return kg[['relation', 'display_relation', 'x_index', 'y_index']].rename(columns={'x_index':'x_idx', 'y_index':'y_idx'})

def create_primekg_edge_index(edges):
    return edges.get(['x_idx', 'y_idx']).values

def create_primekg(nodes: pd.DataFrame, edges: pd.DataFrame):
    df_merged_x = edges.merge(nodes, left_on='x_idx', right_on='node_idx', suffixes=('_x', '_y')) \
                        .drop(columns='x_idx') \
                        .rename(columns={'node_idx':'x_index','node_id': 'x_id', 'node_type': 'x_type', 'node_name': 'x_name', 'node_source': 'x_source'})
    df_merged_final = df_merged_x.merge(nodes, left_on='y_idx', right_on='node_idx', suffixes=('', '_y')) \
                                .drop(columns='y_idx') \
                                .rename(columns={'node_idx':'y_index','node_id': 'y_id', 'node_type': 'y_type', 'node_name': 'y_name', 'node_source': 'y_source'})
    return df_merged_final[['relation', 'display_relation', 'x_index', 'x_id', 'x_type', 'x_name', 'x_source', 'y_index', 'y_id', 'y_type', 'y_name', 'y_source']]
