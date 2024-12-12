import pandas as pd
import argparse

def create_sex_nodes():    
    return pd.DataFrame({
        'name': ['<http://purl.obolibrary.org/obo/NCIT_C20197>', '<http://purl.obolibrary.org/obo/NCIT_C16576>'],
        'type': ['Person', 'Person']
    })
    
def parse_args():
    parser = argparse.ArgumentParser(description="Prepare KG for patient data")
    
    parser.add_argument('nodes_path', type=str, help='Path to the nodes CSV file')
    parser.add_argument('patient_data_path', type=str, help='Path to the patient data CSV file')
    parser.add_argument('-on', '--output_kg_nodes', type=str, help='Path to save the output nodes CSV file')
    
    args = parser.parse_args()
    nodes_path = args.nodes_path
    patient_data_path = args.patient_data_path
    output_kg_nodes = args.output_kg_nodes
    
    return nodes_path, patient_data_path, output_kg_nodes
    
if __name__ == '__main__':
    
    nodes_path, patient_data_path, output_kg_nodes = parse_args()
    nodes = pd.read_csv(nodes_path, low_memory=False)
    
    patient_conn = pd.read_csv(patient_data_path, low_memory=False)
    
    sex_nodes = pd.DataFrame({
        'name': ['<http://purl.obolibrary.org/obo/NCIT_C20197>', '<http://purl.obolibrary.org/obo/NCIT_C16576>'],
        'type': ['Person', 'Person']
    })
    
    nodes = pd.concat([nodes, sex_nodes])
    
    article_nodes = patient_conn[patient_conn['dest_type'] == 'article'].rename(columns={'dest_id': 'name', 'dest_type':'type'})[['name', 'type']].drop_duplicates()
    article_nodes['type'] = 'Article'
    
    nodes = pd.concat([nodes, article_nodes])
    
    if output_kg_nodes:
        print(f"Output saved to {output_kg_nodes}")
        nodes.to_csv(output_kg_nodes, index=False)