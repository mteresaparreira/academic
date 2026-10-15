# academic

Personal academic website of Maria Teresa Parreira, built with Jekyll and served by GitHub Pages.
Based on the [academic-homepage](https://github.com/luost26/academic-homepage) template (MIT license, see `LICENSE`).

Live at: https://mteresaparreira.github.io/academic/

## Where things are

| What | File |
| --- | --- |
| Name, bio, quote, links, education, experience, awards | `_data/profile.yml` |
| Menu items (and hidden pages) | `_data/navigation.yml` |
| Publications (one file each) | `_publications/<year>/*.md` (`selected: true` shows it on the home page) |
| Talks, reviews & committees, code projects, press | `_data/academia.yml` |
| "Log of interesting challenges" | `_data/challenges.yml` |
| Bora / Reboot / Published Thoughts | `other-projects/*.md` |
| CV PDF and profile photo | `docs/cv.pdf`, `docs/profile.jpg` |

### Hidden pages

`publications.html`, `blog.html` (+ `_posts/`), `showcase.html` (+ `_showcase/`) and `index_layout2.html`
are kept from the template for later use. They are built but not linked from the menu;
uncomment them in `_data/navigation.yml` to show them.

## Custom domain

The site is currently served from the `/academic` subpath. When pointing `mariateresaparreira.com` here:

1. Set `baseurl: ""` in `_config.yml`.
2. Add the domain under the repository's Settings → Pages → Custom domain (this creates a `CNAME` file).
3. Update the DNS records at the domain registrar as described in
   [GitHub's docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

Page URLs (`/academia`, `/other-projects/bora`, `/cv`, ...) match the old Google Sites ones, so existing links keep working.

## Running locally

```bash
bundle install
bundle exec jekyll serve
```

## Google Scholar auto-update

`update_publications.py` and `.github/workflows/update-publications.yml` are from the previous site and are
currently not functional (the workflow was failing and GitHub has disabled it). See `SETUP_INSTRUCTIONS.md`.
