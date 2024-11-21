
import igraph as ig
import matplotlib.pyplot as plt
from grape import Graph, GraphVisualizer
from grape.embedders import Node2VecSkipGramEnsmallen
import os
import pandas as pd

def plot_distribution(ax, values, y_scale = 'linear'):   
    ax.set_yscale(y_scale)
    ax.plot(range(0, len(values)), sorted(values, reverse=True))
    ax.set_xticks([])
    

def weighed_hypergraph_node_types(df, layout):
    g = ig.Graph(directed=True)

    nodes = df.columns.append(df.index).tolist()
    g.add_vertices(nodes)
    g.vs['label']=nodes

    edges = [(x, y) for x in df.index for y in df.columns if df.at[x, y] > 0]
    weights = [df.at[x, y] for x, y in edges]
    g.add_edges(edges)
    

    fig, ax = plt.subplots(figsize=(30, 30))
    layout = g.layout(layout)

    edge_colors = [str(w-0.5) for w in weights]
    edge_colors = [f'rgba(0, 0, 0, {w})' for w in edge_colors]
    
    ig.plot(g, target=ax, layout= layout, vertex_size=20,edge_color=edge_colors, edge_width=2, edge_curved=0.2, edge_loop_size=-1.7)

    plt.show()
    
def get_and_save_embedding(graph, name):    
    embedding=Node2VecSkipGramEnsmallen(
                embedding_size=10,
                return_weight=.25,
                explore_weight=4, 
                #change_node_type_weight=.0001,
                #change_edge_type_weight=param[3],
            ).fit_transform(graph)
    emb_file = f'{name}.csv'
    if not os.path.exists(emb_file):
        emb = embedding.fit_transform(graph)
        emb_dump = emb.dump()
        emb_dump['node_embeddings'][0].to_csv(f'{name}.csv', index=False)
    else:
        emb = pd.read_csv(emb_file).to_numpy()
    return emb

def get_grape_graph(nodes, edges, name, directed=True):
    g = Graph.from_pd(
        edges_df = edges,
        nodes_df = nodes,
        node_name_column = 'name',
        node_type_column = 'type',
        edge_src_column = 'object',
        edge_dst_column = 'subject',
        edge_type_column = 'predicate',
        directed =  directed,
        name = name
    )
    return g

def plot_node_type_distribution(type_counts):
    types = list(type_counts.index)
    counts = type_counts.tolist()

    plt.figure(figsize=(8, 12))
    plt.barh(types[::-1], counts[::-1])
    
    plt.xlabel('Types')
    plt.ylabel('Count')
    plt.xscale('log')
    plt.title('Distribution of Types')
    plt.show()
    
def plot_type_distribution_with_components(data):
    ax = data.iloc[::-1].plot.barh(stacked=True, figsize=(10, 20))
    ax.set_xscale('log')
