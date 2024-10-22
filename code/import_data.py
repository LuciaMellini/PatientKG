import requests
from tqdm import tqdm
import os
import argparse

def import_data(url, output_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as file:
        for data in tqdm(response.iter_content(chunk_size=1024), total=total_size//1024, unit='KB'):
            file.write(data)
            
def parse_input():
    parser = argparse.ArgumentParser(description="Import PrimeKG")
    
    parser.add_argument('-o', '--output', type=str, help='Directory to save the PrimeKG CSV file (optional)')
    
    args = parser.parse_args()
    
    return args.output

if __name__ == "__main__":
    
    output_path = parse_input()

    if not os.path.isfile(output_path):
        print("Importing PrimeKG...")
        import_data("https://dataverse.harvard.edu/api/access/datafile/6180620", output_path)
    else:
        print("PrimeKG already exists in the current directory.\n")