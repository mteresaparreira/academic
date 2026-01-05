# Google Scholar Auto-Update Setup Instructions

This guide will help you automatically update your `academia.html` page with publications from your Google Scholar profile.

## 📋 Prerequisites

- Your website is hosted on GitHub Pages from this repository
- You have a Google Scholar profile with publications

## 🔍 Step 1: Find Your Google Scholar ID

1. Go to your Google Scholar profile
2. Look at the URL - it will look something like:
   ```
   https://scholar.google.com/citations?user=XXXXXXXXXX&hl=en
   ```
3. Copy the part after `user=` (before the `&`). This is your Scholar ID.
   - Example: If your URL is `...user=abc123XYZ&hl=en`, your ID is `abc123XYZ`

## 📁 Step 2: Add Files to Your Repository

### 2.1 Add the Python script

1. Copy `update_publications.py` to the root of your repository (same level as `academia.html`)

### 2.2 Add the GitHub Actions workflow

1. In your repository, create a folder path: `.github/workflows/`
2. Copy `update-publications.yml` into this folder
3. Your folder structure should look like:
   ```
   your-repo/
   ├── .github/
   │   └── workflows/
   │       └── update-publications.yml
   ├── academia.html
   ├── update_publications.py
   └── ... other files
   ```

## 🏷️ Step 3: Add HTML Markers to academia.html

Open your `academia.html` file and add these special HTML comments where you want your publications to appear:

```html
<!-- Example placement -->
<section class="publications">
    <h2>Publications</h2>
    
    <!-- PUBLICATIONS_START -->
    <!-- PUBLICATIONS_END -->
    
</section>
```

**Important:** 
- The markers `<!-- PUBLICATIONS_START -->` and `<!-- PUBLICATIONS_END -->` MUST be on their own lines
- Everything between these markers will be replaced with your publications
- You can put any existing content between them initially - it will be replaced on the first run

## 🔐 Step 4: Add Your Google Scholar ID to GitHub Secrets

1. Go to your GitHub repository
2. Click on **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Name: `SCHOLAR_ID`
6. Value: Your Google Scholar ID (from Step 1)
7. Click **Add secret**

## 🎨 Step 5: Add CSS Styling (Optional but Recommended)

Add this to your `style.css` to style the publications nicely:

```css
/* Publications styling */
.publications-list {
    margin-top: 2rem;
}

.publication-item {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e0e0e0;
}

.publication-item:last-child {
    border-bottom: none;
}

.publication-item h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    line-height: 1.4;
}

.publication-item h3 a {
    color: #2563eb;
    text-decoration: none;
}

.publication-item h3 a:hover {
    text-decoration: underline;
}

.publication-item .authors {
    margin: 0.5rem 0;
    color: #4b5563;
    font-size: 0.95rem;
}

.publication-item .venue-info {
    margin: 0.5rem 0 0 0;
    color: #6b7280;
    font-size: 0.9rem;
    font-style: italic;
}

.publication-item .citations {
    color: #059669;
    font-weight: 500;
}
```

## 🚀 Step 6: Test the Setup

### Manual Test (Recommended First)

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click **Update Publications from Google Scholar** workflow
4. Click **Run workflow** button
5. Wait for it to complete (usually 30-60 seconds)
6. Check if your `academia.html` file was updated with your publications

### Automatic Schedule

Once the manual test works:
- The workflow will automatically run **every day at 2 AM UTC**
- You can change this schedule by editing the cron expression in `.github/workflows/update-publications.yml`

Common cron schedules:
```yaml
'0 */6 * * *'   # Every 6 hours
'0 2 * * 1'     # Every Monday at 2 AM
'0 2 1 * *'     # First day of every month at 2 AM
```

## 🔧 Troubleshooting

### "No changes detected" message but publications aren't showing

1. Check that the HTML markers are correctly placed in `academia.html`
2. Make sure the markers are exactly `<!-- PUBLICATIONS_START -->` and `<!-- PUBLICATIONS_END -->`

### Workflow fails with "SCHOLAR_ID not set"

1. Verify you created the secret in GitHub (Step 4)
2. Make sure it's named exactly `SCHOLAR_ID` (case-sensitive)

### Workflow fails with "Error fetching publications"

1. Double-check your Scholar ID is correct
2. Make sure your Google Scholar profile is public
3. Google Scholar may have rate limits - wait a few hours and try again

### Publications not appearing on your live website

1. GitHub Pages can take a few minutes to update after a push
2. Clear your browser cache or try in incognito mode
3. Make sure GitHub Pages is enabled in your repository settings

## 📝 Customizing the Output

You can customize how publications appear by editing the `format_publication_html()` function in `update_publications.py`. The current format includes:

- Title (with link if available)
- Authors
- Venue/Journal
- Year
- Citation count

## 🎯 Example Output

After setup, your publications will appear like this in your HTML:

```html
<!-- PUBLICATIONS_START -->
<!-- Last updated: 2024-01-05 02:00:00 -->
<div class="publications-list">
    <div class="publication-item">
        <h3><a href="..." target="_blank">Your Paper Title</a></h3>
        <p class="authors">Author 1, Author 2, Author 3</p>
        <p class="venue-info">Conference/Journal Name, 2024 • <span class="citations">15 citations</span></p>
    </div>
    <!-- More publications... -->
</div>
<!-- PUBLICATIONS_END -->
```

## 📞 Need Help?

If you run into issues:
1. Check the Actions tab in GitHub for error messages
2. Ensure all files are in the correct locations
3. Verify your Scholar ID is correct and profile is public

Good luck! 🎓
