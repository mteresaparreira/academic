#!/usr/bin/env python3
"""
Local script to update academia.html and automatically push to GitHub
Just run this script and it does everything!
"""

import re
import subprocess
from scholarly import scholarly
from datetime import datetime

# Configuration
GOOGLE_SCHOLAR_ID = "kWYDz2UAAAAJ"  # Replace with your Google Scholar ID
HTML_FILE = "academia.html"
SECTION_MARKER_START = "<!-- PUBLICATIONS_START -->"
SECTION_MARKER_END = "<!-- PUBLICATIONS_END -->"

def run_git_command(command, description):
    """Run a git command and handle errors"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   {e.stderr}")
        return False

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
        
        # Sort by year (most recent first) - handle various year formats
        def get_sort_year(pub):
            year = pub['year']
            if year == 'n.d.' or not year:
                return 0
            # Try to extract just the 4-digit year if there's extra text
            import re
            year_match = re.search(r'(19|20)\d{2}', str(year))
            if year_match:
                return int(year_match.group(0))
            try:
                return int(year)
            except:
                return 0
        
        publications.sort(key=get_sort_year, reverse=True)
        
        # Return top 10
        return publications[:10]
    
    except Exception as e:
        print(f"\n❌ Error fetching publications: {e}")
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
    html += f'            <p class="venue-info">'
    
    # Only show venue if it exists and is not "Unpublished"
    venue = pub['venue']
    if venue and venue != 'Unpublished' and venue.strip():
        html += f'{venue}, '
    
    html += f'{pub["year"]}'
    
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

def push_to_github():
    """Automatically commit and push changes to GitHub"""
    print("\n" + "=" * 60)
    print("Pushing to GitHub...")
    print("=" * 60)
    print()
    
    # Check if there are changes
    result = subprocess.run(
        "git diff --quiet academia.html",
        shell=True,
        capture_output=True
    )
    
    if result.returncode == 0:
        print("ℹ️  No changes detected - publications are already up to date!")
        return True
    
    # Stage the file
    if not run_git_command("git add academia.html", "Staged academia.html"):
        return False
    
    # Commit
    commit_message = f"Update publications - {datetime.now().strftime('%Y-%m-%d')}"
    if not run_git_command(f'git commit -m "{commit_message}"', "Created commit"):
        return False
    
    # Push
    if not run_git_command("git push", "Pushed to GitHub"):
        print("\n⚠️  Push failed. This might be because:")
        print("   1. You need to authenticate (see setup instructions)")
        print("   2. You don't have write access to the repo")
        print("   3. Your branch is behind the remote")
        print("\nYou can manually push with: git push")
        return False
    
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("Google Scholar Publications Updater + Auto-Push")
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
    if not update_html_file(HTML_FILE, new_html):
        return 1
    
    # Push to GitHub
    if push_to_github():
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Your website is updated!")
        print("=" * 60)
        print("\nYour changes are live at:")
        print("https://mteresaparreira.github.io/academic/")
        print("\nGitHub Pages may take 1-2 minutes to rebuild.")
        print()
        return 0
    else:
        print("\n" + "=" * 60)
        print("⚠️  File updated but push failed")
        print("=" * 60)
        print("\nYou can manually push with:")
        print("  git push")
        print()
        return 1

if __name__ == "__main__":
    exit(main())