# CLAUDE.md

## Repository

Hugo blog deployed to **https://hayreddi.github.io** via GitHub Pages + GitHub Actions. Theme: PaperMod.

## Project Structure

- `content/en/posts/` — English blog posts
- `content/tr/posts/` — Turkish blog posts
- `content/{en,tr}/archives.md` — Archive pages
- `content/{en,tr}/search.md` — Search pages
- `static/images/` — Blog post images (organized by post slug)
- `generate_images.py` — Image generation script (Gemini Pro)
- `.github/workflows/deploy.yml` — Auto-deploy on push to main

## Writing Posts

1. Create a markdown file in `content/en/posts/` (or `content/tr/posts/` for Turkish)
2. Use kebab-case filenames (e.g., `build-the-factory-not-the-product.md`)
3. Frontmatter format:
   ```yaml
   ---
   title: "Post Title"
   date: YYYY-MM-DD
   draft: false
   categories: ["Pivot"]
   tags: ["ai", "relevant-tag"]
   summary: "One-line summary shown on homepage."
   ---
   ```
4. Categories: **Pivot**, **Software Stack** (more may be added)
5. Use Turkish characters (ç, ş, ğ, ı, ö, ü, İ, â) properly in Turkish content — never use ASCII-only approximations

## Research Before Writing

Before writing any blog post, always research the topic online first. Search for:
- The latest developments, papers, and discussions on the subject (2025-2026)
- Key people, frameworks, and prior art in the domain
- Existing terminology — use established names rather than inventing new ones
- Contrasting viewpoints and critiques

Ground the post in real sources and include a `## References` table at the bottom with proper attribution. Never write a post based solely on internal knowledge — the goal is to reflect the current state of the field.

## Images

- Generate images using `generate_images.py` which calls **Gemini Pro** (`gemini-3-pro-image-preview`)
- API key is loaded via **AWS Secrets Manager** using the `temp` AWS profile (secret: `stylix/gemini`, region: `us-west-2`)
- Run with: `AWS_PROFILE=temp python3 generate_images.py`
- Save images to `static/images/<post-slug>/`
- Use Hugo figure shortcodes with captions, not plain markdown images:
  ```
  {{< figure src="/images/post-slug/image-name.png" caption="Caption text here." >}}
  ```

## Local Preview

```bash
hugo server --buildDrafts
```
Site runs at http://localhost:1313. Has live reload.

## Publishing

1. Commit changes: `git add <files> && git commit -m "message"`
2. Push: `git push`
3. GitHub Actions auto-builds and deploys — live in ~30 seconds

## Multilingual

- English is the default language (no URL prefix)
- Turkish lives under `/tr/` prefix
- Menu items, descriptions, and all UI text must use native Turkish characters for the TR version

## Memory

When you notice a pattern, preference, or instruction that seems like it will be repeated across future sessions, proactively ask the user: *"Would you like me to save this to memory so I remember it next time?"* before persisting it. This includes things like workflow preferences, tool choices, naming conventions, or any recurring correction.

## Screenshots

Use Playwright for taking browser screenshots when needed:
```python
from playwright.sync_api import sync_playwright
```
