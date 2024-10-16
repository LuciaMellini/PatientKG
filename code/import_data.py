import requests
from tqdm import tqdm
import os

def import_data(url, output_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as file:
        for data in tqdm(response.iter_content(chunk_size=1024), total=total_size//1024, unit='KB'):
            file.write(data)
            
if __name__ == "__main__":
    directory = "./"
    filename = "PrimeKG.csv"

    
    full_path = os.path.join(directory, filename)
    if not os.path.isfile(full_path):
        print("Importing PrimeKG...\n")
        import_data("https://dataverse.harvard.edu/api/access/datafile/6180620", filename)
    else:
        print("PrimeKG already exists in the current directory.\n")