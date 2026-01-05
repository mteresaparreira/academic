#!/usr/bin/env python3
"""
Script to update academia.html with publications from Google Scholar
"""

import os
import re
from scholarly import scholarly
from datetime import datetime

# Configuration
GOOGLE_SCHOLAR_ID = "YOUR_SCHOLAR_ID"  # Replace with your Google Scholar ID
HTML_FILE = "academia.html"
SECTION_MARKER_START = "<!-- PUBLICATIONS_START -->"
SECTION_MARKER_END = "<!-- PUBLICATIONS_END -->"

def get_scholar_id_from_env():
    """Get Scholar ID from environment variable or use default"""
    return os.environ.get('SCHOLAR_ID', GOOGLE_SCHOLAR_ID)

def fetch_publications(scholar_id):
    """Fetch publications from Google Scholar"""
    print(f"Fetching publications for Scholar ID: {scholar_id}")
    
    try:
        # Search for author
        search_query = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(search_query)
        
        # Get publications
        publications = []
        for pub in author['publications']:
            pub_filled = scholarly.fill(pub)
            publications.append({
                'title': pub_filled['bib'].get('title', 'No title'),
                'authors': pub_filled['bib'].get('author', 'Unknown authors'),
                'year': pub_filled['bib'].get('pub_year', 'n.d.'),
                'venue': pub_filled['bib'].get('venue', pub_filled['bib'].get('journal', 'Unpublished')),
                'citations': pub_filled.get('num_citations', 0),
                'url': pub_filled.get('pub_url', pub_filled.get('eprint_url', ''))
            })
        
        # Sort by year (most recent first)
        publications.sort(key=lambda x: int(x['year']) if x['year'] != 'n.d.' else 0, reverse=True)
        
        return publications[:10]
    
    except Exception as e:
        print(f"Error fetching publications: {e}")
        return []

def format_publication_html(pub):
    """Format a single publication as HTML"""
    # Format authors
    authors = pub['authors']
    if isinstance(authors, list):
        authors = ', '.join(authors)
    
    # Create the HTML structure
    html = f'        <div class="publication-item">\n'
    
    if pub['url']:
        html += f'            <h3><a href="{pub["url"]}" target="_blank">{pub["title"]}</a></h3>\n'
    else:
        html += f'            <h3>{pub["title"]}</h3>\n'
    
    html += f'            <p class="authors">{authors}</p>\n'
    html += f'            <p class="venue-info">{pub["venue"]}, {pub["year"]}'
    
    if pub['citations'] > 0:
        html += f' • <span class="citations">{pub["citations"]} citations</span>'
    
    html += '</p>\n'
    html += '        </div>\n'
    
    return html

def generate_publications_html(publications):
    """Generate HTML for all publications"""
    html = f'{SECTION_MARKER_START}\n'
    html += f'    <!-- Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->\n'
    html += '    <div class="publications-list">\n'
    
    for pub in publications:
        html += format_publication_html(pub)
    
    html += '    </div>\n'
    html += f'    {SECTION_MARKER_END}'
    
    return html

def update_html_file(html_file, new_content):
    """Update the HTML file with new publications content"""
    try:
        # Read the current file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if markers exist
        if SECTION_MARKER_START not in content or SECTION_MARKER_END not in content:
            print(f"ERROR: Could not find publication markers in {html_file}")
            print(f"Please add '{SECTION_MARKER_START}' and '{SECTION_MARKER_END}' to your HTML file")
            return False
        
        # Replace content between markers
        pattern = f'{re.escape(SECTION_MARKER_START)}.*?{re.escape(SECTION_MARKER_END)}'
        new_content_full = re.sub(pattern, new_content, content, flags=re.DOTALL)
        
        # Write back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content_full)
        
        print(f"Successfully updated {html_file}")
        return True
    
    except FileNotFoundError:
        print(f"ERROR: File {html_file} not found")
        return False
    except Exception as e:
        print(f"ERROR: Failed to update HTML file: {e}")
        return False

def main():
    """Main function"""
    scholar_id = get_scholar_id_from_env()
    
    if scholar_id == "YOUR_SCHOLAR_ID":
        print("ERROR: Please set your Google Scholar ID")
        print("Either edit GOOGLE_SCHOLAR_ID in this script or set the SCHOLAR_ID environment variable")
        return 1
    
    # Fetch publications
    print("Fetching publications from Google Scholar...")
    publications = fetch_publications(scholar_id)
    
    if not publications:
        print("No publications found or error occurred")
        return 1
    
    print(f"Found {len(publications)} publications")
    
    # Generate HTML
    new_html = generate_publications_html(publications)
    
    # Update HTML file
    if update_html_file(HTML_FILE, new_html):
        print("✓ Publications successfully updated!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())
