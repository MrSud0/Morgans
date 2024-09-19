import argparse
from odf.opendocument import load
from odf.text import P
from logger_setup import setup_logger  # Import the setup_logger function


def modify_odt_content(template_path, output_path, new_text):
    """
    Modify the content of an ODT file using a template.
    """
    logger = setup_logger()
    
    # Load the .odt file as a template
    try:
        template_doc = load(template_path)
        logger.info(f"Loaded template from {template_path}")
    except Exception as e:
        logger.error(f"Failed to load template: {e}")
        return
    
    # Clear existing content
    template_doc.text.childNodes = []
    
    # Add new paragraph with new text
    paragraph = P(text=new_text)
    template_doc.text.addElement(paragraph)
    
    # Save to the specified output path
    try:
        template_doc.save(output_path)
        logger.info(f"Document created: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save document: {e}")

def main():
    # Initialize logger
    logger = setup_logger()

    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate .odt documents from templates.")
    parser.add_argument("type", choices=["benign", "malicious"], help="Type of document to generate.")
    parser.add_argument("--benign-template", default="adv_benign.odt", help="Path to the benign template file.")
    parser.add_argument("--malicious-template", default="adv.odt", help="Path to the malicious template file.")
    parser.add_argument("--output", required=True, help="The output file path for the generated document.")
    
    args = parser.parse_args()

    logger.info(f"Generating a {args.type} document...")

    # Select the correct template based on the type of document
    if args.type == "benign":
        template_path = args.benign_template
        new_text = "Good Document Content"
    elif args.type == "malicious":
        template_path = args.malicious_template
        new_text = "Bad Document Content"
    else:
        logger.error("Invalid document type specified.")
        return
    
    # Generate the document using the specified template and output path
    modify_odt_content(template_path, args.output, new_text)

if __name__ == "__main__":
    main()
