import random
import argparse
import os
import shutil
import odt_generator  # Importing the odt-generator as a module
from logger_setup import setup_logger  # Import the setup_logger function

# Expanded list of example filenames for the generated documents
# TODO add a check to ensure the filename uniqueness 

def find_or_create_output_folder(base_path=".", base_name="odt_folder", overwrite=True):
    """Finds the next available folder name by incrementing a counter and creates the folder if it does not exist.
    If overwrite is True, the existing folder will be removed and recreated."""
    if overwrite:
        folder_path = os.path.join(base_path, base_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Careful, this deletes the folder and everything in it
        os.makedirs(folder_path)
    else:
        i = 0
        while True:
            folder_name = f"{base_name}{i}"
            folder_path = os.path.join(base_path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                break
            i += 1
    return folder_path

def generate_documents(num_files, percentage_malicious, output_folder, file_list):
    if num_files > len(file_list):
        print(f"Maximum of {len(file_list)} files to ensure uniqueness. Please enter a number up to {len(file_list)}.")
        return

    local_file_names = file_list.copy()
    random.shuffle(local_file_names)
    malicious_count = int((percentage_malicious / 100.0) * num_files)
    summary_entries = []

    for _ in range(num_files - malicious_count):
        filename = os.path.join(output_folder, local_file_names.pop() + "_benign.odt")
        odt_generator.modify_odt_content("benign_template.odt", filename, "Good Document Content")
        summary_entries.append(f"{filename}: Benign")

    for _ in range(malicious_count):
        filename = os.path.join(output_folder, local_file_names.pop() + "_malicious.odt")
        odt_generator.modify_odt_content("malicious_template.odt", filename, "Bad Document Content")
        summary_entries.append(f"{filename}: Malicious")

    with open(os.path.join(output_folder, "summary.txt"), "w") as summary_file:
        for entry in summary_entries:
            summary_file.write(f"{entry}\n")

def load_file_names(file_name):
    """Load file names from a file."""
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]

def main():
    parser = argparse.ArgumentParser(description="Generate a mix of benign and malicious .odt documents.")
    parser.add_argument("num_files", type=int, help="The number of files to generate.")
    parser.add_argument("percentage_malicious", type=float, help="The percentage of files that should be malicious.")
    parser.add_argument("--file-list", "-f", type=str, required=True, help="Path to a text file containing a list of filenames to use.")

    args = parser.parse_args()
    
    output_folder = find_or_create_output_folder()
    file_list = load_file_names(args.file_list)
    generate_documents(args.num_files, args.percentage_malicious, output_folder, file_list)

if __name__ == "__main__":
    main()
