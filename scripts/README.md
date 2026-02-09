# Documentation to PDF Synthesis Script

This script automates the process of merging multiple Markdown documentation files into a single, comprehensive PDF document.

## How it works
1. **Merge**: The script reads `docs/_sidebar.md` to determine the correct order of files. It then concatenates them into `docs/Hello-Agents-Full.md`, adding page breaks between sections.
2. **Convert**: It uses `md-to-pdf` (via `npx`) to convert the merged Markdown file into `docs/Hello-Agents-Full.pdf`.

## Requirements
- **Python 3**: For running the merge script.
- **Node.js & npm**: Required to run `md-to-pdf` via `npx`.

## Usage
Simply run the Python script from any location within the project:
```bash
python3 scripts/merge_docs.py
```

## Output Files
- `docs/Hello-Agents-Full.md`: The combined Markdown source.
- `docs/Hello-Agents-Full.pdf`: The final PDF document.
