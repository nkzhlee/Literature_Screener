import bibtexparser
import csv
from datetime import datetime

# Define your search query
#search_term = 'special education AND AI'  # Convert to lower case for case-insensitive matching
search_term = 'large language model AND education'
# Set maximum number of results
max_results = 100  # Adjust as necessary

# Get the current year and calculate the threshold year
current_year = 2025
threshold_year = 2014  # Recent 10 years

# Load and parse the BibTeX file
bibtex_file = 'anthology+abstracts.bib'  # Path to your BibTeX file

try:
    with open(bibtex_file, 'r', encoding='utf-8') as bibtex_file_handle:
        bib_database = bibtexparser.load(bibtex_file_handle)
    print('Successfully loaded the BibTeX file.')
except FileNotFoundError:
    print(f'Error: The BibTeX file {bibtex_file} was not found.')
    exit(1)
except Exception as e:
    print(f'An error occurred while loading the BibTeX file: {e}')
    exit(1)

# Search through the entries
results = []
total_results = 0

print('Searching through the BibTeX entries...')
for entry in bib_database.entries:
    if total_results >= max_results:
        break

    # Extract relevant fields
    title = entry.get('title', '')
    abstract = entry.get('abstract', '')
    year_str = entry.get('year', '')
    authors_list = entry.get('author', '')
    venue = entry.get('booktitle', '') or entry.get('journal', '')
    url = entry.get('url', '')

    # Attempt to convert year to an integer
    try:
        year = int(year_str)
    except ValueError:
        continue  # Skip if year is invalid

    # Check if the publication year is within the recent 10 years
    if not (threshold_year <= year <= current_year):
        continue  # Skip if not within the desired year range

    # Prepare for case-insensitive search
    search_space = ' '.join([title, abstract]).lower()

    # Check if all terms in the search query are present
    search_terms = [term.strip() for term in search_term.split(' AND ')]
    if all(term in search_space for term in search_terms):
        # Build the authors string
        authors = authors_list.replace('\n', ' ').replace('\r', ' ').strip()

        # Append to results
        results.append({
            'title': title,
            'authors': authors,
            'year': str(year),
            'venue': venue,
            'abstract': abstract,
            'url': url
        })
        total_results += 1
        print(f"Found paper: {title}")
    else:
        continue  # Skip if search terms not found

print(f'Total papers found: {len(results)}')

# Write results to CSV
filename = 'acl_anthology_search_results.csv'

with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'authors', 'year', 'venue', 'abstract', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for paper in results:
        writer.writerow(paper)

print(f'Saved {len(results)} papers to {filename}')
