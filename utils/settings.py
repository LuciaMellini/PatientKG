DATA_PATH = "../data/"

NODES_RAW_FILE = DATA_PATH + "nodesL.csv"
EDGES_RAW_FILE = DATA_PATH + "edgesL.csv"

SAVE_PREPARED = True
NODES_PREPARED_FILE = DATA_PATH + "nodes.csv"
EDGES_PREPARED_FILE = DATA_PATH + "edges.csv"

OMIM_MONDO_MAP = DATA_PATH + "omim_MONDO_MAP.txt"

SAVE_WITH_PATIENT_FILES = True
NODES_WITH_PATIENT_FILE = DATA_PATH + "nodes_with_patients.csv"
EDGES_WITH_PATIENT_FILE = DATA_PATH + "edges_with_patients.csv"

PATIENT_PATH = DATA_PATH + "patient_data.csv"
SAVE_PATIENT_CONNECTIONS = True
PATIENT_CONNECTIONS = DATA_PATH + "patient_connections.csv"
SAVE_PATIENT_FEATURES = True
PATIENT_FEATURES = DATA_PATH + "patient_features.csv"

SAVE_FILTERED_FILES = True
NODES_FILTERED_FILE = DATA_PATH + "nodes_filtered.csv"
EDGES_FILTERED_FILE = DATA_PATH + "edges_filtered.csv"

NODE_TYPES_TO_KEEP = ['Gene','Genomic feature','Protein','Disease','GO', 'Phenotype', 'Article', 'Person']
NODE_TYPES_TO_RENAME = {'Gene': 'Genomic feature'}

 
HPO_MAP_NOT_IN_KG = {
    '<http://purl.obolibrary.org/obo/HP_0030214>': {"HPO_id": 'HP:5200321', "label": 'Amplification of sexual behavior'},
    '<http://purl.obolibrary.org/obo/HP_0002355>': {"HPO_id":'HP:0001288', "label":'Gait disturbance'},
    '<http://purl.obolibrary.org/obo/HP_0006919>': {"HPO_id":'HP:0000718', "label":'Aggressive behaviour'}
}
