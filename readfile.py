import os
import csv

# Specify the directory path
folder_path = 'C:\PDF-20240903T135637Z-001\PDF'

# Get a list of all files in the directory
file_names = os.listdir(folder_path)

# Specify the CSV file where you want to save the filenames
output_csv = 'C:\PDF-20240903T135637Z-001\PDF\output_filenames.csv'

# Write the filenames to the CSV file
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename'])  # Write the header
    for file_name in file_names:
        writer.writerow([file_name])

print(f"Filenames written to {output_csv}")