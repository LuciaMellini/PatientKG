purl_to_id =  lambda s: s.split("/")[-1].replace('_', ':')[:-1]

def get_node_types_for_edge_type(edges, nodes, edge_type):
    edges_with_types = edges[edges['predicate'] == edge_type]
    
    source_types = edges_with_types.merge(
        nodes[['name', 'type']], 
        left_on='subject',
        right_on='name'
    )['type'].value_counts()
        
    
    target_types = edges_with_types.merge(
        nodes[['name', 'type']],
        left_on='object', 
        right_on='name'
    )['type'].value_counts()
    
    node_type_counts = source_types.add(target_types, fill_value=0)
    node_type_counts.name = edge_type
    
    return node_type_counts.sort_values(ascending=False)


def get_n_edges_for_node_type(edges, nodes):
    edges_with_node_type = edges.merge(nodes[['name', 'type']], left_on='subject', right_on='name', how='left')
    edges_with_node_type = edges_with_node_type.rename(columns={'type': 'x_type'}).drop(columns=['name'])
    edges_with_node_type = edges_with_node_type.merge(nodes[['name', 'type']], left_on='object', right_on='name', how='left')
    edges_with_node_type = edges_with_node_type.rename(columns={'type': 'y_type'}).drop(columns=['name'])
    return edges_with_node_type.groupby(['x_type', 'y_type']).size().unstack(fill_value=0)