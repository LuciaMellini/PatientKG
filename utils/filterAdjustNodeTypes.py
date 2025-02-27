import argparse
import pandas as pd
from settings import *
from KG_utils import *

if __name__ == '__main__':
    output_nodes, output_edges = False, False
    
    nodes = pd.read_csv(NODES_WITH_PATIENT_FILE, low_memory=False)
    edges = pd.read_csv(EDGES_WITH_PATIENT_FILE,  low_memory=False)
    node_types = nodes['type'].unique()
    
    node_types_to_remove = [t for t in node_types if t not in NODE_TYPES_TO_KEEP]
    node_types_to_rename = NODE_TYPES_TO_RENAME

    
    nodes_kept, edges_kept = nodes, edges
    for t in node_types_to_remove:
        print("Removing nodes of type", t)
        nodes_kept, edges_kept = remove_node_type(nodes_kept, edges_kept, t)
    print(f"Removed {len(nodes) - len(nodes_kept)} nodes\n")
        
    nodes = nodes_kept
    edges = edges_kept
    
    nodes_renamed = nodes
    for old_t, new_t in node_types_to_rename.items():
        print('Renaming nodes of type', old_t, 'to', new_t)
        nodes_renamed = rename_node_type(nodes_renamed, old_t, new_t)  
    print(f"Renamed {len(nodes) - len(nodes_renamed)} nodes\n")
        
    nodes = nodes_renamed  
        
    if SAVE_FILTERED_FILES:
        nodes.to_csv(NODES_FILTERED_FILE, index=False)
        print(f"Output nodes saved to {NODES_FILTERED_FILE}")
        edges.to_csv(NODES_FILTERED_FILE, index=False)
        print(f"Output edges saved to {EDGES_FILTERED_FILE}")
        
    
        
    