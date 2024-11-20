python preparePatientData.py ./data/patient_data.csv -oc ./data/patient_connections.csv -of ./data/patient_features.csv

echo Adding missing HPOs to knowledge graph
python addMissingHPOs.py

echo Mapping OMIM ids to MONDO ids
python omimMondoMap.py

echo Merging patients to knowledge graph
python patientJoin.py ./data/nodesL.csv ./data/edgesL.csv ./data/patient_data.csv -okgn ./data/nodes_with_patients.csv -okge ./data/edges_with_patients.csv 
