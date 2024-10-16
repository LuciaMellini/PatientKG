import requests
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import igraph as ig


def create_node_df(kg):
    nodes = pd.concat([kg.get(['x_id','x_type', 'x_name','x_source']).rename(columns={'x_id':'node_id', 'x_type':'node_type', 'x_name':'node_name','x_source':'node_source'}), 
                   kg.get(['y_id','y_type', 'y_name','y_source']).rename(columns={'y_id':'node_id', 'y_type':'node_type', 'y_name':'node_name','y_source':'node_source'})])
    nodes = nodes.drop_duplicates().reset_index().drop('index',axis=1).reset_index().rename(columns={'index':'node_idx'})
    return nodes

def create_edge_df(kg, nodes):
    edges = pd.merge(kg, nodes, 'left', left_on=['x_id','x_type', 'x_name','x_source'], right_on=['node_id','node_type','node_name','node_source'])
    edges = edges.rename(columns={'node_idx':'x_idx'})
    edges = pd.merge(edges, nodes, 'left', left_on=['y_id','y_type', 'y_name','y_source'], right_on=['node_id','node_type','node_name','node_source'])
    edges = edges.rename(columns={'node_idx':'y_idx'})
    edges = edges.get(['relation', 'display_relation','x_idx', 'y_idx'])
    return edges

def create_edge_index(edges):
    return edges.get(['x_idx', 'y_idx']).values

def dfs_to_graph(nodes, edges):
    graph = ig.Graph()

    graph.add_vertices(nodes['node_idx'])
    for attribute in nodes.columns:
        graph.vs[attribute] = nodes[attribute]
        
    edge_index = create_edge_index(edges)
    graph.add_edges([tuple(x) for x in edge_index])
    for attribute in edges.columns:
        graph.es[attribute] = edges[attribute]

    graph = graph.as_undirected(mode='collapse')
            

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
    plt.figure(figsize=(13,8))
    G = nx.DiGraph()
    for x_node in df.index:
        for y_node in df.columns:
            weight = df.loc[x_node, y_node]
            if weight > 0:
                G.add_edge(x_node, y_node, weight=weight)
                
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

    nx.draw_networkx_nodes(G, pos, node_size=200, node_color='lightblue')
    edge_weights = [d['weight'] for (_, _, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, arrowstyle='->', width=[w / 10 for w in edge_weights], edge_color="gray", connectionstyle=f'arc3,rad={radius}', arrowsize=15)

    nx.draw_networkx_labels(G, pos, labels=new_labels, font_size=10)

    plt.axis('off')
    plt.show()


def clustering_info(graph, clustering_method_func):
    clustering = clustering_method_func()
    membership = clustering.membership

    num_communities = len(set(membership))
    modularity_score = graph.modularity(membership)
    return num_communities, modularity_score