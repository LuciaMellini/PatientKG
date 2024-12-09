
import igraph as ig
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import cm
from matplotlib.patches import Arc
from grape import Graph, GraphVisualizer
from grape.embedders import Node2VecSkipGramEnsmallen
import os
import pandas as pd
import random
import networkx as nx
from math import log

def plot_distribution(ax, values, x_scale = 'linear', y_scale = 'linear'):   
    ax.set_xscale(x_scale)
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

def weighed_hypergraph_node_types_per_edge_types(df):
    G = nx.from_pandas_edgelist(
        df, 'type_subject', 'type_object', ['predicate', 'Count'], create_using=nx.DiGraph()
    )

    pos = nx.circular_layout(G)

    pos['Phenotype'], pos['Disease'] = pos['Disease'], pos['Phenotype']
    if 'Gene' in pos:
        pos['Gene'], pos['Genomic feature'] = pos['Genomic feature'], pos['Gene']

    plt.figure(figsize=(10, 7))

    node_order = list(G.nodes)[::-1]
    nx.draw_networkx_nodes(G, pos, nodelist = node_order,node_size=200, node_color="lightblue")

    predicates = {predicate: i for i, predicate in enumerate(df['predicate'].unique())}
    cmap = cm.get_cmap('tab10', len(predicates))
    simple_colors = [cmap(i) for i in range(cmap.N)]
    predicate_colors = {predicate: simple_colors[i % len(simple_colors)] for i, predicate in enumerate(df['predicate'].unique())}

    random.seed(123)
    edge_weights = df['Count'].values
    edge_weights_scaled = [.2*log(weight) for weight in edge_weights]
    
    get_index_multiple_loop = (df[(df['type_subject'] == df['type_object']) & (df.duplicated(['type_subject', 'type_object'], keep=False))]
                                .groupby('type_subject').agg(
        Indices=('type_subject', lambda x: list(x.index))
    ).reset_index())
    repeated_loops_idx = sum([l[1:] for l in get_index_multiple_loop['Indices'].values],[])
    # Draw edges with custom curvature for loops and non-loops with increased curvature
   
    for idx, row in df.iterrows():
        if idx not in repeated_loops_idx:
            source = row['type_subject']
            target = row['type_object']
            predicate = row['predicate']
            
            # Determine edge color based on predicate
            color = predicate_colors.get(predicate, "gray")

            curvature = random.uniform(0.2, 0.6)
            nx.draw_networkx_edges(
                G, pos, edgelist=[(source, target)], 
                connectionstyle=f"arc3,rad={curvature}", edge_color=color, arrows=True, arrowstyle='-|>',
                label=predicate, width = edge_weights_scaled[idx]
            )
            
    # manage multiple self-loops
    for idx in repeated_loops_idx:  
        x, y = pos[df.at[idx, 'type_subject']]
        # Draw a self-loop using an Arc
        loop = Arc(
            (x-0.05, y), 0.1, 0.2, angle=0,   # Center of the arc and its size
            theta1=20, theta2=-20,  # Start and end angles (half-circle)
            color=simple_colors[predicates[df.at[idx, 'predicate']]], zorder=1, lw= edge_weights_scaled[idx]
        )
        plt.gca().add_patch(loop)

    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    legend_handles = [Line2D([0], [0], color=color, lw=4, label=predicate) for predicate, color in predicate_colors.items()]

    plt.legend(handles=legend_handles, loc='best', title="Predicate Types")
    plt.axis('off')
    plt.show()
    
def get_embedding(graph, emb_file_name = None):    
    emb_file = f'{emb_file_name}.csv'
    if not os.path.exists(emb_file):
        embedding=Node2VecSkipGramEnsmallen(
                    embedding_size=10,
                    return_weight=.25,
                    explore_weight=4, 
                    #change_node_type_weight=.0001,
                    #change_edge_type_weight=param[3],
                )
    
        emb = embedding.fit_transform(graph)
        emb_dump = emb.dump()
        emb_dump['node_embeddings'][0].to_csv(emb_file, index=False)
    else:
        emb = pd.read_csv(emb_file).to_numpy()
    return emb

def visualize_embedding(emb, g):
    vis = GraphVisualizer(
                graph=g,
                automatically_display_on_notebooks=False,
                decomposition_method = 'TSNE',
            )
    vis.fit_nodes(emb)
    vis.plot_node_types()
    plt.show()

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
