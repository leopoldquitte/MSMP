import os
import csv
import re

# Function to parse a PDB file and extract atom coordinates
def parse_pdb_file(pdb_file):
    coordinates = []
    with open(pdb_file, 'r') as file:
        for line in file:
            if line.startswith('ATOM'):
                residue_name = line[17:20].strip()
                residue_number = int(line[22:26].strip())
                atom_name = line[12:16].strip()
                try:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    coordinates.append((residue_name, residue_number, atom_name, x, y, z))
                except ValueError:
                    print(f"Skipping line in {pdb_file} due to missing or invalid coordinate: {line.strip()}")
    return coordinates

# Function to generate the CSV file from parsed coordinates
def generate_csv_from_pdb(output_csv):
    all_columns = set()
    pdb_pattern = re.compile(r'^frame\.pdb\.\d+$')
    current_directory = os.getcwd()

    # First pass: Collect all columns (residues and atoms)
    for pdb_file in os.listdir(current_directory):
        if pdb_pattern.match(pdb_file):
            file_path = os.path.join(current_directory, pdb_file)
            coordinates = parse_pdb_file(file_path)
            for coord in coordinates:
                residue_name, residue_number, atom_name, x, y, z = coord
                all_columns.update([
                    (residue_name, residue_number, atom_name, 'x'),
                    (residue_name, residue_number, atom_name, 'y'),
                    (residue_name, residue_number, atom_name, 'z')
                ])

    # Sort the columns
    sorted_columns = sorted(all_columns, key=lambda x: (x[1], x[0], x[2], x[3]))
    header = ['PDB_File'] + [f'{residue_name}{residue_number}{atom_name}{coord}' for residue_name, residue_number, atom_name, coord in sorted_columns]

    # Write to CSV with streaming processing (process each PDB file one by one)
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        for pdb_file in os.listdir(current_directory):
            if pdb_pattern.match(pdb_file):
                file_path = os.path.join(current_directory, pdb_file)
                coordinates = parse_pdb_file(file_path)
                row = {col: '' for col in header}
                row['PDB_File'] = pdb_file

                for coord in coordinates:
                    residue_name, residue_number, atom_name, x, y, z = coord
                    row[f'{residue_name}{residue_number}{atom_name}x'] = x
                    row[f'{residue_name}{residue_number}{atom_name}y'] = y
                    row[f'{residue_name}{residue_number}{atom_name}z'] = z
                
                # Write the row for this PDB file
                writer.writerow(row)

# Output CSV file
output_csv_file = 'output_coordinates.csv'

# Generate the CSV file
generate_csv_from_pdb(output_csv_file)

