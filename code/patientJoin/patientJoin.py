import os

if __name__ == "__main___":
    if not os.path.exists('nodes_with_ids.csv'):
        print("nodes_with_ids.csv does not exist")
    else:
        os.system('python3 id_unification.py')
        
    