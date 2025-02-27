import subprocess
import os

def print_colored_header(message):
    # Using ANSI escape codes for underlined text
    print(f"\033[4m{message}\033[0m")

# Current directory where the scripts are located
script_dir = os.path.dirname(os.path.abspath(__file__))

# List of scripts to run with their headers
steps = [
    ("Preparing patient data", "preparePatientData.py"),
    ("Preparing knowledge graph", "prepareKG.py"),
    ("Adding missing HPOs to knowledge graph", "addMissingHPOs.py"),
    ("Merging patients to knowledge graph", "patientJoin.py"),
    ("Filtering and adjusting node types", "filterAdjustNodeTypes.py")
 ]

# Execute each script in sequence
for header, script in steps:
    print_colored_header(header)
    script_path = os.path.join(script_dir, script)
    subprocess.run(['python', script_path], check=True)
    print()  # Empty line between steps