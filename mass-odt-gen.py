import subprocess
import random
import argparse
import os
import shutil


# Expanded list of example filenames for the generated documents
# TODO update the tool to integrate the functionality of the odt-generator.py instead of calling it externally
# TODO update the tool to receive a list from a file, use a named argument for that
# TODO add a check to ensure the filename uniqueness 

file_names = [
    "finance_report", "sales_forecast", "annual_summary", "meeting_minutes",
    "strategy_outline", "project_plan", "budget_review", "employee_handbook",
    "customer_survey", "market_research", "investment_plan", "product_launch",
    "training_manual", "policy_update", "performance_review", "audit_results",
    "compliance_checklist", "risk_assessment", "tech_upgrade_proposal",
    "partnership_agreement", "quarterly_analysis", "sustainability_report",
    "feedback_summary", "crisis_management_plan", "innovation_strategy",
    "digital_transformation", "competitive_analysis", "customer_insights",
    "revenue_projections", "expansion_plan", "brand_strategy", "user_guide",
    "service_catalog", "event_plan", "content_calendar", "campaign_analysis",
    "workshop_outline", "onboarding_guide", "maintenance_schedule",
    "procurement_list", "security_protocol", "disaster_recovery_plan",
    "legal_contract", "HR_policy", "IT_inventory", "project_timeline",
    "meeting_agenda", "sales_pitch", "business_model", "growth_strategy",
    "market_trends_analysis"
]

def find_or_create_output_folder(base_path=".", base_name="odt_folder", overwrite=True):
    """Finds the next available folder name by incrementing a counter and creates the folder if it does not exist.
    If overwrite is True, the existing folder will be removed and recreated."""
    if overwrite:
        folder_path = os.path.join(base_path, base_name)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Careful yo this deletes the folder and everything in it
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


def generate_documents(num_files, percentage_malicious, output_folder):
    if num_files > 50:
        print("Maximum of 50 files to ensure uniqueness. Please enter a number up to 50.")
        return

    local_file_names = file_names.copy()
    random.shuffle(local_file_names)
    malicious_count = int((percentage_malicious / 100.0) * num_files)
    summary_entries = []

    for _ in range(num_files - malicious_count):
        filename = os.path.join(output_folder, local_file_names.pop() + "_benign.odt")
        subprocess.run(["python", "odt-generator.py", "benign", "--benign-template", "adv_benign.odt", "--output", filename], check=True)
        summary_entries.append(f"{filename}: Benign")

    for _ in range(malicious_count):
        filename = os.path.join(output_folder, local_file_names.pop() + "_malicious.odt")
        subprocess.run(["python", "odt-generator.py", "malicious", "--malicious-template", "adv.odt", "--output", filename], check=True)
        summary_entries.append(f"{filename}: Malicious")

    with open(os.path.join(output_folder, "summary.txt"), "w") as summary_file:
        for entry in summary_entries:
            summary_file.write(f"{entry}\n")

def main():
    parser = argparse.ArgumentParser(description="Generate a mix of benign and malicious .odt documents.")
    parser.add_argument("num_files", type=int, help="The number of files to generate, up to a maximum of 50 to ensure uniqueness.")
    parser.add_argument("percentage_malicious", type=float, help="The percentage of files that should be malicious.")
    
    args = parser.parse_args()
    
    output_folder = find_or_create_output_folder()
    generate_documents(args.num_files, args.percentage_malicious, output_folder)

if __name__ == "__main__":
    main()
