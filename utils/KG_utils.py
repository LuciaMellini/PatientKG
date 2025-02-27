import pandas as pd

def get_node_types_count_for_edge_type(nodes, edges, edge_type):
    edges_with_types = edges[edges['predicate'] == edge_type]
    edges_with_node_types = edges_with_types.merge(
        nodes[['name', 'type']], 
        left_on='object',
        right_on='name'
    ).merge(
        nodes[['name', 'type']], 
        left_on='subject',
        right_on='name',
        suffixes = ('_object', '_subject')

    ).drop(columns = ['name_object', 'name_subject', 'subject', 'object'])
    
    
    return edges_with_node_types.groupby(list(edges_with_node_types.columns)).size().reset_index(name='Count')

def create_sex_nodes():    
    return pd.DataFrame({
        'name': ['<http://purl.obolibrary.org/obo/NCIT_C20197>', '<http://purl.obolibrary.org/obo/NCIT_C16576>'],
        'type': ['Person', 'Person']
    })
    

def get_n_edges_for_node_type(edges, nodes):
    edges_with_node_type = edges.merge(nodes[['name', 'type']], left_on='subject', right_on='name', how='left')
    edges_with_node_type = edges_with_node_type.rename(columns={'type': 'x_type'}).drop(columns=['name'])
    edges_with_node_type = edges_with_node_type.merge(nodes[['name', 'type']], left_on='object', right_on='name', how='left')
    edges_with_node_type = edges_with_node_type.rename(columns={'type': 'y_type'}).drop(columns=['name'])
    return edges_with_node_type.groupby(['x_type', 'y_type']).size().unstack(fill_value=0)

def remove_node_type(nodes, edges, node_type):
    nodes_filtered = nodes[nodes['type'] != node_type]
    edges_filtered = edges[edges['subject'].isin(nodes_filtered['name']) & edges['object'].isin(nodes_filtered['name'])]
    return nodes_filtered, edges_filtered

def remove_node(nodes, edges, node_name):
    nodes_filtered = nodes[nodes['name'] != node_name]
    edges_filtered = edges[(edges['subject'] != node_name) & (edges['object'] != node_name)]
    return nodes_filtered, edges_filtered

def rename_node_type(nodes, old_type, new_type):
    nodes.loc[nodes['type'] == old_type, 'type'] = new_type
    return nodes

def add_nodes(nodes, new_nodes):
    return pd.concat([nodes, new_nodes])

def add_edges(edges, new_edges):
    return pd.concat([edges, new_edges])