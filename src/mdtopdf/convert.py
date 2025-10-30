"""The main module for converting markdown files to PDF"""

import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

import requests
from abllib import fs, log
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from playwright.sync_api import Page, sync_playwright

logger = log.get_logger("main")

# install playwright browsers
os.system("playwright install chromium")

def convert(filename: str) -> None:
    """
    Convert the given Markdown file to PDF.
    """

    log.initialize(log.LogLevel.INFO)
    log.add_console_handler()

    filename = fs.absolute(filename)

    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    with tempfile.TemporaryDirectory() as tdir:
        name = Path(filename).stem

        md_file = fs.absolute(tdir, name + ".md")
        _copy_md_file(filename, md_file, tdir)

        css_file = fs.absolute(tdir, "github_style.css")
        if shutil.which("github-markdown-css") is not None:
            _generate_style_css(css_file)
        else:
            _download_style_css(css_file)

        html_file = fs.absolute(tdir, name + ".html")
        _generate_html(md_file, html_file, css_file)

        pdf_file = fs.absolute(tdir, name + ".pdf")
        _generate_pdf(f"file:///{html_file}", pdf_file)

        final_file = fs.absolute(os.path.dirname(filename), name + ".pdf")
        shutil.copyfile(pdf_file, final_file)

def _copy_md_file(filename: str, md_file: str, tdir: str) -> None:
    shutil.copyfile(filename, md_file)

    with open(md_file, "r", encoding="utf8") as f:
        content = f.read()

    for match in re.findall(r"!\[.+\]\((.+)\)", content):
        logger.info(f"including image file {match}")

        if os.path.dirname(match) != "":
            img_dir = fs.absolute(tdir, os.path.dirname(match))
            os.makedirs(img_dir, exist_ok=True)

        orig_img = fs.absolute(os.path.dirname(filename), match)
        if not os.path.isfile(orig_img):
            logger.warning(f"source image file {match} wasn't found, ignoring it. full path: {orig_img}")
            continue

        img_file = fs.absolute(tdir, match)
        shutil.copyfile(orig_img, img_file)

def _generate_style_css(css_file: str) -> None:
    logger.info("Generating the newest Github markdown style sheet")

    res = os.system(f"github-markdown-css --theme=dark_dimmed > {css_file}")
    if res != 0:
        logger.error(f"{css_file} could not be created")
        sys.exit(1)

def _download_style_css(css_file: str) -> None:
    logger.info("Downloading Github markdown style sheet")

    r = requests.get("https://raw.githubusercontent.com/sindresorhus/github-markdown-css"
                     "/refs/heads/main/github-markdown-dark.css",
                     timeout=30)
    with open(css_file, "wb") as f:
        f.write(r.content)

def _generate_html(md_file: str, html_file, css_file: str) -> None:
    md = MarkdownIt("commonmark", {"html": True}) \
                    .use(front_matter_plugin) \
                    .use(footnote_plugin) \
                    .enable('table')

    with open(md_file, "r", encoding="utf8") as f:
        raw_html = md.render(f.read())

    prefix = HTML_PREFIX.replace("F1L3N4M3H3R3", Path(md_file).name) \
                        .replace("STYLE_F1L3_H3R3", css_file)

    suffix = HTML_SUFFIX

    with open(html_file, "w+", encoding="utf8") as f:
        f.write(prefix + raw_html + suffix)

def _generate_pdf(url: str, pdf_path: str) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(url)

        height = _get_page_height(page)
        page.pdf(
            path=pdf_path,
            print_background=True,
            height=f"{height}px",
            page_ranges="1"
        )

        logger.info(f"Generated file {Path(pdf_path).name}")

        browser.close()

def _get_page_height(page: Page) -> float:
    """
    Code from here:
    https://stackoverflow.com/a/70355152/15436169
    """

    return page.evaluate('''() => {
        const body = document.body
        const html = document.documentElement;
        return Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
    }''')

HTML_PREFIX = """
<!DOCTYPE html>
<html>
<head>
<title>F1L3N4M3H3R3</title>
<meta http-equiv="Content-type" content="text/html;charset=UTF-8">
<link rel="stylesheet" href="STYLE_F1L3_H3R3">
<style>
.markdown-body {
	box-sizing: border-box;
	min-width: 200px;
	max-width: 980px;
	margin: 0 auto;
	padding: 45px;
}

@media (max-width: 767px) {
	.markdown-body {
		padding: 15px;
	}
}
</style>
</head>
<body class="markdown-body">
"""

HTML_SUFFIX = """
</body>
</html>
"""
