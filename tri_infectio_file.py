import os
import csv

# Directory and file configuration
source_dir = "AllBiomodels.xml"
output_csv = "sorted_infectious_index.csv"

# Define classification categories for sorting
categories = {
    "Viral": ["virus", "sars-cov-2", "hiv", "aids", "influenza", "flu", "ebola", "zika"],
    "Bacterial": ["bacteria", "tuberculosis", "cholera", "sepsis", "pneumonia"],
    "Parasitic": ["parasite", "malaria", "leishmaniasis", "trypanosoma"],
    "General_Infection": ["infection", "pathogen", "immune", "epidemic", "transmission"]
}

print(f"Starting classification in {source_dir}...")

with open(output_csv, "w", newline='') as f:
    writer = csv.writer(f)
    # Writing the CSV header
    writer.writerow(["File", "Category", "Keyword_Found"])

    # Iterate through each file in the source directory
    for filename in os.listdir(source_dir):
        if filename.endswith(".xml"):
            file_path = os.path.join(source_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as xml_file:
                    content = xml_file.read().lower()
                    
                    # Check keywords for each category
                    for category, keywords in categories.items():
                        for word in keywords:
                            if word in content:
                                writer.writerow([filename, category, word])
                                # Move to the next file once a match is found
                                break 
            except Exception as e:
                print(f"Error processing {filename}: {e}")

print(f"Done! Sorting index saved to: {output_csv}")