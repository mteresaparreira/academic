# academic

Personal academic website of Maria Teresa Parreira, built with Jekyll and served by GitHub Pages.
Based on the [academic-homepage](https://github.com/luost26/academic-homepage) template (MIT license, see `LICENSE`).

Live at: https://mteresaparreira.github.io/academic/

## Where things are

| What | File |
| --- | --- |
| Name, bio, quote, links, education, experience, awards | `_data/profile.yml` |
| Menu items (and hidden pages) | `_data/navigation.yml` |
| Publications (one file each) | `_publications/<year>/*.md` |
| News on the home page (one file each) | `_news/*.md` |
| Which home-page sections are shown | `_data/display.yml` |
| Teaching, organizing committees, talks, reviews, code projects, press (Academia page) | `_data/academia.yml` |
| "Log of interesting challenges" | `_data/challenges.yml` |
| Bora / Reboot / Published Thoughts | `other-projects/*.md` |
| CV PDF and profile photo | `docs/cv.pdf`, `docs/profile.jpg` |

### Hidden pages

`publications.html`, `blog.html` (+ `_posts/`), `showcase.html` (+ `_showcase/`) and `index_layout2.html`
are kept from the template for later use. They are built but not linked from the menu;
uncomment them in `_data/navigation.yml` to show them.

## Customizing the home page

The home page (`index.html`) keeps all the template's sections. Each one is filled from a data file:

| Section | Where it comes from | How to change it |
| --- | --- | --- |
| **Profile card** (left column: photo, name, positions, email, icons) | `_data/profile.yml` | `portrait_url` is the photo; `positions` are the lines under the name; `email`, `gscholar`, `github`, `linkedin`, `twitter`, `orcid` add the icons (comment a line out with `#` to remove its icon). |
| **About Me** (bio + quote + CV link) | `short_bio` and `cv_link` in `_data/profile.yml` | `short_bio` is HTML: use `<p>...</p>` for paragraphs and `<a href="...">` for links. |
| **Education / Experience / Honors & Awards** | `education`, `experience`, `awards` in `_data/profile.yml` | Each entry has `name`, `position`, `date` and an optional `logo` (image in `assets/images/badges/`, about 128×128 px). Without a logo, a small icon is shown. Add `show_on_home: false` to an experience entry to list it only on the Academia page. Delete a whole list to hide that column. |
| **News** | one file per item in `_news/` | Copy an existing file, change `title` (HTML allowed) and `date`. Newest first; only the month is shown. `num_news` in `_data/display.yml` sets how many appear. |
| **Selected Publications** | files in `_publications/` with `selected: true` | See [Highlighting publications](#highlighting-publications). |

Turn any section on or off in `_data/display.yml` (`show_experience`, `show_news`, `show_selected_publications`).

The yellow warning box at the top of the page only appears if `baseurl` in `_config.yml` doesn't match where the site
is served (e.g. after switching to the custom domain). The template's other warning, which asks you to rename the
repository to `<username>.github.io`, was removed from `index.html` because the `academic` name is intentional.

## Highlighting publications

Each publication is a Markdown file in `_publications/<year>/`. All of them are listed on the Academia page,
grouped by year. To feature one on the home page and make it stand out:

```yaml
---
title:          'Robot Duck Debugging: Can Attentive Listening Improve Problem Solving?'
date:           2023-10-09 00:01:00 -0500   # used for ordering (newest first)
selected:       true                         # show under "Selected Publications" on the home page
pub:            'Proceedings of the 25th International Conference on Multimodal Interaction (ICMI)'
pub_post:       ', pp. 527–536'              # text after the venue (optional)
pub_date:       "2023"
abstract: >-
  One or two sentences shown under the venue.   # optional, keep it short
cover:          /assets/images/covers/duck.jpg  # optional thumbnail; without it a colourful
                                                # bubble pattern is generated
pub_last:       ' <span class="badge badge-pill badge-publication badge-success">Best Paper</span>'  # optional badge
authors:
  - Maria Teresa Parreira*      # * = equal contribution
  - Sarah Gillet*
  - Iolanda Leite#              # # = corresponding author
links:
  Paper: https://...
  Code: https://github.com/...
  Video: https://...
---
```

- **`selected: true`** is what puts a paper on the home page.
- **Cover images** go in `assets/images/covers/` (around 300×200 px, landscape).
- **Badges:** change `badge-success` (green) to `badge-primary` (blue), `badge-warning` (yellow), `badge-danger` (red)
  or `badge-info` (teal), and the text to anything ("Oral", "Spotlight", "Honorable Mention", ...).
- **Your name is bold** because of `_data/authors.yml`. You can add co-authors there with a `url` to link their names.
- **Links** can have any label; each one becomes a `[Label]` button.
- **Citation counts:** add `semantic_scholar_id: <id>` (the long ID at the end of the paper's Semantic Scholar URL)
  and the count appears next to the venue.

### Adding new publications from Google Scholar

On your Scholar profile, select papers → Export → CSV. Then create one file per new paper in
`_publications/<year>/` using the format above (copy an existing file). Scholar exports titles in lower case and
sometimes lists the same paper twice (preprint + published version), so check those by hand.

## Custom domain

The site is currently served from the `/academic` subpath. When pointing `mariateresaparreira.com` here:

1. Set `baseurl: ""` in `_config.yml`.
2. Add the domain under the repository's Settings → Pages → Custom domain (this creates a `CNAME` file).
3. Update the DNS records at the domain registrar as described in
   [GitHub's docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

Page URLs (`/academia`, `/other-projects/bora`, `/cv`, ...) match the old Google Sites ones, so existing links keep working.

## Previewing the site on your computer

You need Ruby once (Ubuntu): `sudo apt install ruby-full ruby-bundler build-essential`.
Then, in this folder:

```bash
bundle config set --local path vendor/bundle   # first time only: keep gems inside this folder
bundle install                                  # first time only
bundle exec jekyll serve                         # then open http://127.0.0.1:4000/academic/
```

The site rebuilds when you save a file; refresh the browser to see it (restart the command after editing `_config.yml`).
Stop it with Ctrl+C.

## Google Scholar auto-update

`update_publications.py` and `.github/workflows/update-publications.yml` are from the previous site and are
currently not functional (the workflow was failing and GitHub has disabled it). See `SETUP_INSTRUCTIONS.md`.
