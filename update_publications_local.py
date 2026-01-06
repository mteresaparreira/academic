#!/usr/bin/env python3
"""
Local script to update academia.html with publications from Google Scholar
Run this on your laptop - it will update your local academia.html file
"""

import re
from scholarly import scholarly
from datetime import datetime

# Configuration
GOOGLE_SCHOLAR_ID = "kWYDz2UAAAAJ"  # Replace with your Google Scholar ID
HTML_FILE = "academia.html"
SECTION_MARKER_START = "<!-- PUBLICATIONS_START -->"
SECTION_MARKER_END = "<!-- PUBLICATIONS_END -->"

def fetch_publications(scholar_id):
    """Fetch publications from Google Scholar"""
    print(f"Fetching publications for Scholar ID: {scholar_id}")
    print("This may take 30-60 seconds...")
    
    try:
        # Search for author
        search_query = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(search_query)
        
        print(f"Found author: {author.get('name', 'Unknown')}")
        print(f"Total publications: {len(author.get('publications', []))}")
        
        # Get publications
        publications = []
        for i, pub in enumerate(author['publications'], 1):
            print(f"Fetching publication {i}/{len(author['publications'])}...", end='\r')
            pub_filled = scholarly.fill(pub)
            
            publications.append({
                'title': pub_filled['bib'].get('title', 'No title'),
                'authors': pub_filled['bib'].get('author', 'Unknown authors'),
                'year': pub_filled['bib'].get('pub_year', 'n.d.'),
                'venue': pub_filled['bib'].get('venue', pub_filled['bib'].get('journal', 'Unpublished')),
                'citations': pub_filled.get('num_citations', 0),
                'url': pub_filled.get('pub_url', pub_filled.get('eprint_url', ''))
            })
        
        print()  # New line after progress
        
        # Sort by year (most recent first)
        publications.sort(key=lambda x: int(x['year']) if x['year'] != 'n.d.' else 0, reverse=True)
        
        # Return top 10
        return publications[:10]
    
    except Exception as e:
        print(f"\nError fetching publications: {e}")
        print("\nTroubleshooting:")
        print("- Make sure your Google Scholar ID is correct")
        print("- Try running again in a few minutes")
        print("- Check your internet connection")
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
            print(f"\n❌ ERROR: Could not find publication markers in {html_file}")
            print(f"Please add these lines to your HTML file where you want publications:")
            print(f"  {SECTION_MARKER_START}")
            print(f"  {SECTION_MARKER_END}")
            return False
        
        # Replace content between markers
        pattern = f'{re.escape(SECTION_MARKER_START)}.*?{re.escape(SECTION_MARKER_END)}'
        new_content_full = re.sub(pattern, new_content, content, flags=re.DOTALL)
        
        # Write back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content_full)
        
        print(f"\n✅ Successfully updated {html_file}")
        return True
    
    except FileNotFoundError:
        print(f"\n❌ ERROR: File {html_file} not found")
        print("Make sure you're running this script in the same folder as your academia.html file")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: Failed to update HTML file: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Google Scholar Publications Updater (Local Version)")
    print("=" * 60)
    print()
    
    # Fetch publications
    publications = fetch_publications(GOOGLE_SCHOLAR_ID)
    
    if not publications:
        print("\n❌ No publications found or error occurred")
        return 1
    
    print(f"\n✅ Found {len(publications)} publications")
    
    # Show what we found
    print("\nPublications to be added:")
    for i, pub in enumerate(publications, 1):
        print(f"  {i}. {pub['title']} ({pub['year']})")
    
    print()
    
    # Generate HTML
    new_html = generate_publications_html(publications)
    
    # Update HTML file
    if update_html_file(HTML_FILE, new_html):
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Your academia.html has been updated.")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review the changes in academia.html")
        print("2. Commit and push to GitHub:")
        print("   git add academia.html")
        print("   git commit -m 'Update publications'")
        print("   git push")
        print()
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())