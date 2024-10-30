# Literature Screener
This is a rapid research literature screener that is used to find the related paper by keywords.

## 1. Set Up Conda Python Environment
To set up the Conda environment with the required dependencies, follow these steps:

```sh
conda create --name literature_screener_env python=3.9
conda activate literature_screener_env
pip install scholarly requests beautifulsoup4 pandas pybtex
```
## 2. Documentation of Python Codes
### google_scholar_screener.py
This script is used to perform literature screening using Google Scholar. It utilizes the scholarly library to retrieve academic articles based on specific queries. The results are then processed and saved for further analysis.

Key Features:

Fetches articles from Google Scholar based on a given keyword or query.
Saves metadata (e.g., title, authors, abstract) of the retrieved articles in a structured format.

### ACL_Screener.py
This script is designed to screen articles from the ACL Anthology. It processes metadata and filters articles based on predefined criteria, saving relevant information for further review.

Key Features:

Downloads and processes metadata from the ACL Anthology.
Filters articles using user-defined criteria and saves the results.

## Merge the result

### merge_processor.py
This script processes .bib files from ACM and IEEE, combines them with an existing Excel file of research papers, and outputs a merged Excel file. It handles potential duplicate entries and extracts key metadata from the BibTeX entries, such as title, author, publication year, venue, and more.


## Result 
The results from the literature screening are saved in the results directory. Each script generates a CSV file that contains metadata such as article titles, authors, publication year, and abstracts, which can be used for further analysis.
