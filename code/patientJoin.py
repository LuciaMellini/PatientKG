import argparse
import pandas as pd

def parse_input():
    parser = argparse.ArgumentParser(description="Merge patient data with PrimeKG")
    
    parser.add_argument('node_path', type=str, help='Path to the KG node CSV file')
    parser.add_argument('edge_path', type=str, help='Path to the KG edge CSV file')
    parser.add_argument('patient_data_path', type=str, help='Path to the patient connection data CSV file')
    
    parser.add_argument('-okgn', '--output_kg_nodes', type=str, help='Path to save the output kg nodes CSV file (optional)')
    parser.add_argument('-okge', '--output_kg_edges', type=str, help='Path to save the output kg edges CSV file (optional)')

    
    args = parser.parse_args()
    node_path = args.node_path
    edge_path = args.edge_path
    patient_data_path = args.patient_data_path
    output_kg_nodes = args.output_kg_nodes
    output_kg_edges = args.output_kg_edges
    
    return node_path, edge_path, patient_data_path, output_kg_nodes, output_kg_edges

def create_patient_nodes(patient_conn):
    patient_nodes = []
    for _, row in patient_conn[['patient_id']].iterrows():
        patient_nodes.append({
            'name': row['patient_id'],
            'type': 'Patient'
        })
    return pd.DataFrame(patient_nodes)

def create_patient_edges(patient_conn, nodes):
    nodes['name_copy'] =  nodes['name']
    nodes['name'] = nodes['name'].apply(purl_to_id)
    edges_new = nodes.merge(patient_conn, left_on = 'name', right_on = 'dest_id')
    print(edges_new.head8)
    return pd.DataFrame()
    
def create_kg_with_patients(nodes, edges, patient_conn):
    patient_nodes = create_patient_nodes(patient_conn)
    new_nodes = pd.concat([nodes, patient_nodes])
    patient_edges = create_patient_edges(patient_conn, new_nodes)
    return new_nodes, pd.concat([edges, patient_edges])
    
if __name__=='__main__':

    node_path, edge_path, patient_data_path, output_kg_nodes, output_kg_edges = parse_input()
        
    print("Reading KG...") 
    nodes = pd.read_csv(node_path, low_memory=False)
    edges = pd.read_csv(edge_path, low_memory=False)
    
    patient_conn = pd.read_csv(patient_data_path, low_memory=False)
    
    #create_kg_with_patients(nodes, edges, patient_conn)