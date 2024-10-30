from scholarly import scholarly
import csv
import time
from datetime import datetime
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define the search term
# Use Boolean operator to better control your searches
# Searches are not case sensitive, however, there are a number of Boolean operators you can use to control the search and these must be capitalized.
#
# AND requires both of the words or phrases on either side to be somewhere in the record.
# NOT can be placed in front of a word or phrases to exclude results which include them.
# OR will give equal weight to results which match just one of the words or phrases on either side.
search_term = '"Special Education" AND "AI"'

# Optional: Add a timestamp to your filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'search_results_{timestamp}.csv'

with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'author', 'pub_year', 'venue', 'abstract', 'num_citations', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Initialize the search query
    search_query = scholarly.search_pubs(search_term)

    # Set a limit on the number of results (adjust as needed)
    max_results = 500  # Google Scholar typically allows up to 1000 results

    for i, publication in enumerate(tqdm(search_query, total=max_results)):
        if i >= max_results:
            break  # Stop after reaching the max_results limit

        # Try to extract the necessary fields
        try:
            print(publication)
            bib = publication.get('bib', {})
            title = bib.get('title', '')
            author = ', '.join(bib.get('author', []))
            pub_year = bib.get('pub_year', '')
            venue = bib.get('venue', '')
            abstract = bib.get('abstract', '')
            num_citations = publication.get('num_citations', 0)
            url = publication.get('pub_url', '')

            # Write the data to CSV
            writer.writerow({
                'title': title,
                'author': author,
                'pub_year': pub_year,
                'venue': venue,
                'abstract': abstract,
                'num_citations': num_citations,
                'url': url
            })
        except Exception as e:
            logging.error(f"Error processing publication {i + 1}: {e}")

        # Optional: Add a delay to prevent rate limiting
        time.sleep(1)

print(f"Data has been written to {filename}")
