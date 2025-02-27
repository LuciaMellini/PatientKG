
import networkx as nx
import pandas as pd
import pickle
from grape import Graph
from collections import Counter
from settings import *

if __name__ == '__main__':
    # Generate Dataframes
    nodes_df = pd.read_csv(NODES_RAW_FILE, header=0)
    edges_df = pd.read_csv(EDGES_RAW_FILE, header=0)


    graph = Graph.from_pd(
        edges_df=edges_df,
        nodes_df=nodes_df,
        node_name_column="name",
        node_type_column="type",
        edge_src_column="subject",
        edge_dst_column="object",
        #edge_weight_column="weight",
        edge_type_column="predicate",
        node_types_separator="|",
        directed=False,
        name="hpo_1",
    )

    # load it into a graph
    digraph = Graph.from_pd(
        edges_df=edges_df,
        nodes_df=nodes_df,
        node_name_column="name",
        node_type_column="type",
        edge_src_column="subject",
        edge_dst_column="object",
        #edge_weight_column="weight",
        edge_type_column="predicate",
        node_types_separator="|",
        directed=True,
        name="hpo_0",
    )

    ontological_relations= edges_df[edges_df.predicate=='Subclassof']
    #ontological_relations

    #Add extreme types
    ontological_relations.loc[:,'type_subject'] = ontological_relations['subject'].apply(lambda id: graph.get_node_type_names_from_node_name(id)[0])
    ontological_relations.loc[:,'type_object'] = ontological_relations['object'].apply(lambda id: graph.get_node_type_names_from_node_name(id)[0])
    
    for selected_type in nodes_df['type'].unique():
        filtered_nodes_df = nodes_df.loc[nodes_df['type'] == selected_type]
        filtered_edges_df = ontological_relations.loc[(ontological_relations['type_subject'] == selected_type) & (ontological_relations['type_object'] == selected_type)]

        # Put relations in a file
        filtered_edges_df[['subject','object']].to_csv('ontological_relations.tsv', sep='\t',index=False, header=False)

        filtered_graph = Graph.from_pd(
            edges_df=filtered_edges_df,
            nodes_df=filtered_nodes_df,
            node_name_column="name",
            node_type_column="type",
            edge_src_column="subject",
            edge_dst_column="object",
            #edge_weight_column="weight",
            edge_type_column="predicate",
            node_types_separator="|",
            directed=False,
            name="filtered_graph",
        )
        G = nx.DiGraph()        
                
                # Add nodes from the 'source' and 'target' columns
        G.add_nodes_from(filtered_nodes_df['name'])

        # Add edges from the DataFrame
        edges = [(row['subject'], row['object']) for index, row in filtered_edges_df.iterrows()]
        G.add_edges_from(edges)

        # #Verify if any cycle
        # for cycle in nx.simple_cycles(G):
        #     print(cycle)

        # Connected components
        Counter(filtered_graph.get_connected_components()[0])
        
        # Create transitive closure 
        Gtc = nx.transitive_closure(G)
        #Gtc = G

        pickle.dump(Gtc, open(f"transitive_closure_{selected_type.lower()}_G.p", 'wb'))
        # Sizes of connected components
        # Gcc = sorted(nx.connected_components(Gtc.to_undirected()), key=len, reverse=True)
        # print(f'Sizes of connected components: {[len(g) for g in Gcc]}')