# Markdown to PDF

Convert a markdown file to PDF using Github Dark Dimmed styling.

## Usage

Open a new command prompt window and run the following command:
```bash
md-to-pdf your_markdown_file.md
```
or
```bash
python -m markdown-2-pdf.convert your_markdown_file.md
```

After a few seconds, a new pdf file with the name of the original file should appear.

## Installation

### PyPI

All stable versions get released on [PyPI](https://pypi.org/project/markdown-2-pdf). To download the newest version, run the following command:
```bash
pip install markdown-2-pdf
```
This will automatically install all other dependencies.

Alternatively, a specific version can be installed as follows:
```bash
pip install markdown-2-pdf==1.0.0
```
where 1.0.0 is the version you want to install.

### Github

To install the latest development version directly from Github, run the following command:
```bash
pip install git+https://github.com/Ableytner/markdown-to-pdf.git
```

Additionally, a [wheel](https://peps.python.org/pep-0427/) is added to every [stable release](https://github.com/Ableytner/markdown-to-pdf/releases), which can be manually downloaded and installed.

### requirements.txt

If you want to include this library as a dependency in your requirements.txt, the syntax is as follows:
```text
markdown-2-pdf==1.0.0
```
where 1.0.0 is the version that you want to install.

To always use the latest stable version:
```text
markdown-2-pdf
```

To always install the latest development version:
```text
markdown-2-pdf @ git+https://github.com/Ableytner/markdown-to-pdf
```

## Use latest Github styling

If you want to use the latest Github markdown styling, this package also provides a way to accomplish that.

First, you need to [install npm and Node.js](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

Install the [generate-github-markdown-css](https://github.com/sindresorhus/generate-github-markdown-css) library, which is used to generate the Github styling:
```bash
npm install --global generate-github-markdown-css
```

The library will now automatically generate and use the newest Github styling.
