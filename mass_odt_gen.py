import random
import argparse
import os
import shutil
import odt_generator  # Importing the odt_generator as a module
from logger_setup import setup_logger  # Import the setup_logger function

# Expanded list of example filenames for the generated documents
# TODO add a check to ensure the filename uniqueness 

def find_or_create_output_dir(base_path=".", base_name="odt_dir", overwrite=True):
    """Finds the next available directory name by incrementing a counter and creates the directory if it does not exist.
    If overwrite is True, the existing directory will be removed and recreated."""
    if overwrite:
        dir_path = os.path.join(base_path, base_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)  # Careful, this deletes the directory and everything in it
        os.makedirs(dir_path)
    else:
        i = 0
        while True:
            dir_name = f"{base_name}{i}"
            dir_path = os.path.join(base_path, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                break
            i += 1
    return dir_path

def generate_documents(num_files, percentage_malicious, output_dir, file_list):
    if num_files > len(file_list):
        print(f"Maximum of {len(file_list)} files to ensure uniqueness. Please enter a number up to {len(file_list)}.")
        return

    local_file_names = file_list.copy()
    random.shuffle(local_file_names)
    malicious_count = int((percentage_malicious / 100.0) * num_files)
    summary_entries = []

    for _ in range(num_files - malicious_count):
        filename = os.path.join(output_dir, local_file_names.pop() + "_benign.odt")
        odt_generator.modify_odt_content("benign_template.odt", filename, "Good Document Content")
        summary_entries.append(f"{filename}: Benign")

    for _ in range(malicious_count):
        filename = os.path.join(output_dir, local_file_names.pop() + "_malicious.odt")
        odt_generator.modify_odt_content("malicious_template.odt", filename, "Bad Document Content")
        summary_entries.append(f"{filename}: Malicious")

    with open(os.path.join(output_dir, "summary.txt"), "w") as summary_file:
        for entry in summary_entries:
            summary_file.write(f"{entry}\n")

def load_file_names(file_name):
    """Load file names from a file."""
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]

def main():
    logger = setup_logger()  # Initialize the logger
    parser = argparse.ArgumentParser(description="Generate a mix of benign and malicious .odt documents.")
    parser.add_argument("num_files", type=int, help="The number of files to generate.")
    parser.add_argument("percentage_malicious", type=float, help="The percentage of files that should be malicious.")
    parser.add_argument("--file-list", "-f", type=str, required=True, help="Path to a text file containing a list of filenames to use.")

    args = parser.parse_args()
    
    output_dir = find_or_create_output_dir()
    file_list = load_file_names(args.file_list)
    generate_documents(args.num_files, args.percentage_malicious, output_dir, file_list)
    logger.info(f"Generated {args.num_files} files with {args.percentage_malicious}% malicious content.")

if __name__ == "__main__":
    main()
