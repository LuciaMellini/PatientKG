echo -e "\033[4mPreparing patient data\033[0m"
python preparePatientData.py 

echo -e "\n\033[4mPreparing knowledge graph\033[0m"
python prepareKG.py 

echo -e "\n\033[4mAdding missing HPOs to knowledge graph\033[0m"
python addMissingHPOs.py

echo -e "\n\033[4mMerging patients to knowledge graph\033[0m"
python patientJoin.py 

echo -e "\n\033[4mFiltering and adjusting node types\033[0m"
python filterAdjustNodeTypes.py 