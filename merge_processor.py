import pandas as pd
from pybtex.database import parse_file, BibliographyData, BibliographyDataError

# Load and parse the BibTeX file with duplicates handling
def parse_bib_file_no_duplicates(bib_path):
    try:
        bib_data = parse_file(bib_path)
    except BibliographyDataError as e:
        print(f"Error parsing {bib_path}: {e}")
        return BibliographyData(entries={})

    unique_entries = {}
    for key, entry in bib_data.entries.items():
        if key not in unique_entries:
            unique_entries[key] = entry
        else:
            # Rename duplicate keys to make them unique
            new_key = f"{key}_duplicate"
            unique_entries[new_key] = entry

    return BibliographyData(entries=unique_entries)

# File paths
acm_bib_path = './results/ACM.bib'
ieee_bib_path = './results/IEEE.bib'
excel_file_path = './results/search_results_LLMandSED.xlsx'

# Parse the .bib files with duplicate handling
acm_bib_data = parse_bib_file_no_duplicates(acm_bib_path)
ieee_bib_data = parse_bib_file_no_duplicates(ieee_bib_path)

# Function to convert bib data to a pandas DataFrame
def bib_to_dataframe(bib_data):
    rows = []
    for key, entry in bib_data.entries.items():
        title = entry.fields.get('title', '')
        author = ', '.join(
            f"{person.first_names[0] if person.first_names else ''} {person.last_names[0] if person.last_names else ''}".strip() for person in entry.persons['author']
        ) if 'author' in entry.persons else ''
        year = entry.fields.get('year', '')
        venue = entry.fields.get('booktitle', entry.fields.get('journal', ''))
        abstract = entry.fields.get('abstract', '')
        url = entry.fields.get('url', '')
        num_citations = 0  # This information is not available in bib files, so default to 0

        rows.append({
            'title': title,
            'author': author,
            'pub_year': year,
            'venue': venue,
            'abstract': abstract,
            'num_citations': num_citations,
            'url': url
        })

    return pd.DataFrame(rows)

# Convert both ACM and IEEE bib data to dataframes
acm_df = bib_to_dataframe(acm_bib_data)
ieee_df = bib_to_dataframe(ieee_bib_data)

# Combine the two bib dataframes
combined_bib_df = pd.concat([acm_df, ieee_df], ignore_index=True)

# Load the existing Excel file
existing_df = pd.read_excel(excel_file_path)

# Merge the combined bib dataframe with the original excel data
merged_df = pd.concat([existing_df, combined_bib_df], ignore_index=True)

# Save the merged data to a new Excel file
merged_df.to_excel('merged_paper_list.xlsx', index=False)

# Display the first few rows of the merged data
print(merged_df.head())
