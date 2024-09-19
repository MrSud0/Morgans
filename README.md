# ODT Document Generator

This repository contains two Python scripts designed for working with ODT (OpenDocument Text) files. These tools allow you to generate, encrypt, obfuscate, and serve ODT files, which can be particularly useful in scenarios requiring document manipulation or security-focused operations.

## Scripts Overview

### 1. `odt-generator.py`

This script is designed to generate ODT documents from templates, either benign or malicious, depending on the user's input. It modifies the content of the ODT files based on the type specified and outputs the result to a designated location.

#### Features:
- Generates ODT files using either benign or malicious templates.
- Allows for command-line specification of templates and output paths.

#### Usage:
```bash
python odt-generator.py [type] --output <output_path> [--benign-template <path>] [--malicious-template <path>]
```

#### Arguments:
- `type`: The type of document to generate. Options are `benign` or `malicious`.
- `--benign-template`: Path to the benign template file. Default is `adv_benign.odt`.
- `--malicious-template`: Path to the malicious template file. Default is `adv.odt`.
- `--output`: The output file path for the generated document (required).

#### Example:
```bash
python odt-generator.py benign --output output.odt
```

### 2. `mass-odt-enc-obf.py`

This script provides a comprehensive solution for processing multiple ODT files. It includes features for encrypting specified patterns within ODT files, obfuscating text, and even serving files via a simple HTTP server.

#### Features:
- Encrypts specific patterns within ODT files using XOR encryption.
- Obfuscates variable names, functions, and specific strings in StarBasic code within ODT files.
- Moves benign ODT files to a separate directory after processing.
- Zips the processed files into a single archive.
- Serves the current directory over HTTP.

#### Usage:
```bash
python mass-odt-enc-obf.py --dir <folder_path> [options]
```

#### Arguments:
- `--dir` or `-d`: Directory containing the ODT files to process (required).
- `--macro-dir` or `-md`: Directory within the ODT file where the macro is located. Default is `Basic/Standard`.
- `--macro-file` or `-mf`: The macro file to encrypt within the ODT files. Default is `Module1.xml`.
- `--obfuscate` or `-obf`: Enables the obfuscation of strings and variables.
- `--encrypt-strings` or `-es`: File containing patterns for encryption.
- `--obfuscate-strings` or `-os`: File containing patterns for obfuscation.
- `--obfuscate-vars` or `-ov`: Enables the obfuscation of variable names in the code.

#### Example:
```bash
python mass-odt-enc-obf.py --dir ./odt_files --encrypt-strings enc_strings.txt --obfuscate --obfuscate-vars
```

#### Additional Features:
- Serve the current directory over HTTP after processing with the following command:
```bash
python mass-odt-enc-obf.py --dir ./odt_files --obfuscate
```
  
## Installation

To use these scripts, you need to have Python installed on your system along with the required packages. You can install the dependencies using the following command:

```bash
pip install odfpy
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
