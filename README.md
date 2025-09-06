# Markdown to PDF

Convert a markdown file to PDF using Github Dark Dimmed styling.

## Usage

Open a new command prompt window and run the following command:
```bash
mdtopdf your_markdown_file.md
```
or
```bash
python -m mdtopdf your_markdown_file.md
```

After a few seconds, a new pdf file with the name of the original file should appear.

## Installation

### PyPI

This project is currently not published on PyPI because all combinations of markdown-to-pdf / mdtopdf are already taken.

### Github

To install the latest development version directly from Github, run the following command:
```bash
pip install git+https://github.com/Ableytner/markdown-to-pdf.git
```

Additionally, a [wheel](https://peps.python.org/pep-0427/) is added to every [stable release](https://github.com/Ableytner/markdown-to-pdf/releases), which can be manually downloaded and installed, or installed with the following command:
```bash
pip install git+https://github.com/Ableytner/markdown-to-pdf/releases/download/1.0.0/markdown-to-pdf-1.0.0.tar.gz
```
where 1.0.0 is the version you want to install.

### requirements.txt

If you want to include this library as a dependency in your requirements.txt, the syntax is as follows:
```text
mdtopdf @ git+https://github.com/Ableytner/markdown-to-pdf/releases/download/1.0.0/markdown-to-pdf-1.0.0.tar.gz
```
where 1.0.0 is the version that you want to install.

Alternatively, to always install the latest development version:
```text
mdtopdf @ git+https://github.com/Ableytner/markdown-to-pdf
```

## Use latest Github styling

If you want to use the latest Github markdown styling, this package also provides a way to accomplish that.

First, you need to [install npm and Node.js](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

Install the [generate-github-markdown-css](https://github.com/sindresorhus/generate-github-markdown-css) library, which is used to generate the Github styling:
```bash
npm install --global generate-github-markdown-css
```

The library will now automatically generate and use the newest Github styling.
