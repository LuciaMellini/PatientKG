import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import igraph as ig
import sys
sys.path.append('..')
from PrimeKG_utils import create_primekg_edge_index



def dfs_to_graph(nodes, edges):
    graph = ig.Graph()

    graph.add_vertices(nodes['node_idx'])
    for attribute in nodes.columns:
        graph.vs[attribute] = nodes[attribute]
        
    edge_index = create_primekg_edge_index(edges)
    graph.add_edges([tuple(x) for x in edge_index])
    for attribute in edges.columns:
        graph.es[attribute] = edges[attribute]

    graph = graph.as_undirected(mode='collapse')
    return graph
            

def plot_degree_distribution(ax, graph, node_type):
    neighbor_counts = [len(graph.neighbors(node)) for node in graph.vs.select(node_type=node_type) if len(graph.neighbors(node))>30]
    
    ax.bar(range(len(neighbor_counts)), sorted(neighbor_counts, reverse = True), linewidth = 0.1)
    ax.set_title(f"Node type: {node_type}, (number of edges: {sum(neighbor_counts)})")
    ax.set_ylabel('Number of neighbors')
    
    ax.set_xlim(-len(neighbor_counts)/50, len(neighbor_counts))
    ax.set_ylim(0, max(neighbor_counts))
    
    ax.set_xticks([])
    max_height = max(neighbor_counts)
    if max_height > 0:
        ax.axhline(y=max_height, color='grey', linestyle='--', linewidth=0.8)

    current_ticks = ax.get_yticks().tolist()    
    if max_height not in current_ticks:
        current_ticks.append(max_height)
    ax.set_yticks(current_ticks)    
    current_tick_labels = [int(tick) for tick in current_ticks]
    ax.set_yticklabels(current_tick_labels)
    
def links_per_node_type(edge_index, nodes):
    edges_with_node_type = pd.DataFrame(edge_index, columns=['x_idx', 'y_idx'])
    edges_with_node_type = edges_with_node_type.merge(nodes[['node_idx', 'node_type']], left_on='x_idx', right_on='node_idx', how='left')
    edges_with_node_type = edges_with_node_type.rename(columns={'node_type': 'x_node_type'}).drop(columns=['node_idx'])
    edges_with_node_type = edges_with_node_type.merge(nodes[['node_idx', 'node_type']], left_on='y_idx', right_on='node_idx', how='left')
    edges_with_node_type = edges_with_node_type.rename(columns={'node_type': 'y_node_type'}).drop(columns=['node_idx'])

    return edges_with_node_type.groupby(['x_node_type', 'y_node_type']).size().unstack(fill_value=0)

def weighed_hypergraph_node_types(df, radius):
    edges = [
        ('drug', 'disease'), ('drug', 'gene/protein'), 
        ('exposure', 'disease'), ('exposure', 'biological_process'), 
        ('exposure', 'cellular_component'), ('exposure', 'molecular_function'), 
        ('gene/protein', 'biological_process'), ('gene/protein', 'cellular_component'), 
        ('gene/protein', 'molecular_function'), ('disease', 'gene/protein'), 
        ('effect/phenotype', 'disease'), ('effect/phenotype', 'gene/protein'), 
        ('gene/protein', 'anatomy'), ('gene/protein', 'pathway')
    ]

    g = ig.Graph()

    nodes = df.index.tolist()
    g.add_vertices(nodes)

    edges = [(x, y) for x in df.index for y in df.columns if df.at[x, y] > 0]
    # Remove duplicate edges considering (x, y) and (y, x) as the same edge
    #edges = list(set(tuple(sorted(edge)) for edge in edges))
    weights = [df.at[x, y] for x, y in edges]
    g.add_edges(edges)

    new_labels = {
        "drug": "drugs",
        "exposure": "exposures",
        "disease": "diseases",
        "effect/phenotype": "phenotypes", 
        "gene/protein": "genes", 
        "anatomy": "anatomical\n regions", 
        "pathway": "pathways",
        "cellular_component": "CC", 
        "molecular_function": "MF", 
        "biological_process": "BP"
    }

    # Define the positions for each node
    pos = {
        "drug": (0, 3), 
        "exposure": (4, 3),
        "disease": (1, 1.5), 
        "effect/phenotype": (0, 0), 
        "gene/protein": (4, 0), 
        "anatomy": (3, -1), 
        "pathway": (5, -1),
        "cellular_component": (5, 2), 
        "molecular_function": (4, 2), 
        "biological_process": (3, 2)
    }

    # Set node colors (optional: to match your previous example)
    color_dict = {
        'drug': 'brown', 'disease': 'yellow', 'effect/phenotype': 'pink', 'exposure': 'lightyellow',
        'gene/protein': 'purple', 'pathway': 'lightpink', 'anatomy': 'red',
        'biological_process': 'orange', 'cellular_component': 'coral', 'molecular_function': 'salmon'
    }
    colors = [color_dict[node] for node in nodes]

    # Convert pos dictionary to a list of tuples matching igraph layout format
    layout = [pos[node] for node in nodes]

    # Plot the graph using the predefined layout
    fig, ax = plt.subplots(figsize=(8, 8))
    min_weight, max_weight = min(weights), max(weights)
    normalized_weights = [(w - min_weight) / (max_weight - min_weight) for w in weights]


    edge_colors = [str(w) for w in normalized_weights]
    edge_colors = [f'rgba(0, 0, 0, {w})' for w in edge_colors]
    ig.plot(g, target=ax, layout=layout, vertex_label=[new_labels[node] for node in nodes], vertex_color=colors, 
            vertex_size=40, edge_color=edge_colors, edge_width=3, edge_curved=radius, edge_loop_size=-1.5)

    plt.show()

def clustering_info(graph, clustering_method_func):
    clustering = clustering_method_func()
    membership = clustering.membership

    num_communities = len(set(membership))
    modularity_score = graph.modularity(membership)
    return num_communities, modularity_score