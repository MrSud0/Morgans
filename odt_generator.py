import argparse
from odf.opendocument import load
from odf.text import P

def modify_odt_content(template_path, output_path, new_text):
    # Load the .odt file as a template
    template_doc = load(template_path)
    
    # Clear existing content
    template_doc.text.childNodes = []
    
    # Add new paragraph with new text
    paragraph = P(text=new_text)
    template_doc.text.addElement(paragraph)
    
    # Save to the specified output path
    template_doc.save(output_path)
    print(f"Document created: {output_path}")

def main():
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate .odt documents from templates.")
    parser.add_argument("type", choices=["benign", "malicious"], help="Type of document to generate.")
    parser.add_argument("--benign-template", default="adv_benign.odt", help="Path to the benign template file.")
    parser.add_argument("--malicious-template", default="adv.odt", help="Path to the malicious template file.")
    parser.add_argument("--output", required=True, help="The output file path for the generated document.")
    
    args = parser.parse_args()
    
    # Select the correct template based on the type of document
    if args.type == "benign":
        template_path = args.benign_template
        new_text = "Good Document Content"
    elif args.type == "malicious":
        template_path = args.malicious_template
        new_text = "Bad Document Content"
    else:
        print("Invalid document type specified.")
        return
    
    # Generate the document using the specified template and output path
    modify_odt_content(template_path, args.output, new_text)

if __name__ == "__main__":
    main()
