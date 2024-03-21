# Markdown to PDF

Convert a markdown file to a PDF using Github Dark Dimmed styling.

## Usage

Open a new command prompt window and navigate to the folder containing the markdown file to be converted. Then run the following command:
```bash
python -m markdowntopdf your_markdown_file.md
```

After a few seconds, a new pdf file with the name of the original file should appear.

## Install

Install the project directly from Github:
```bash
pip install git+https://github.com/Ableytner/markdown-to-pdf.git
```

Install [generate-github-markdown-css](https://github.com/sindresorhus/generate-github-markdown-css) library, which is used to generate the Github-specific style.css:
```bash
npm install --global generate-github-markdown-css
```
