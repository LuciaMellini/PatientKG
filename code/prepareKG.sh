echo -e "\033[4mPreparing patient data\033[0m"
python preparePatientData.py ./data/patient_data.csv -oc ./data/patient_connections.csv -of ./data/patient_features.csv

echo -e "\n\033[4mPreparing knowledge graph\033[0m"
python prepareKG.py ./data/nodesL.csv ./data/patient_connections.csv -on ./data/nodes.csv

echo -e "\n\033[4mAdding missing HPOs to knowledge graph\033[0m"
python addMissingHPOs.py

echo -e "\n\033[4mMerging patients to knowledge graph\033[0m"
python patientJoin.py ./data/nodes.csv ./data/edges.csv ./data/patient_connections.csv -okgn ./data/nodes_with_patients.csv -okge ./data/edges_with_patients.csv 

echo -e "\n\033[4mFiltering and adjusting node types\033[0m"
python filterAdjustNodeTypes.py ./data/nodes_with_patients.csv ./data/edges_with_patients.csv -on ./data/nodes_filtered.csv -oe ./data/edges_filtered.csv