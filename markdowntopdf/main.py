import os
# set chromium version to fix download issue
# https://github.com/pyppeteer/pyppeteer/issues/463
os.environ["PYPPETEER_CHROMIUM_REVISION"] = "1267552"

import asyncio
import shutil
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from pyppeteer import launch
from pyppeteer.page import Page

CSS_FILENAME = "github_dark_dimmed_style.css"

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        raise Exception("No filename provided")

    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    if not os.path.isabs(filename):
        filename = os.path.join(os.getcwd(), filename)

    _generate_style_css()

    html_filename = _generate_html(filename)

    asyncio.get_event_loop().run_until_complete(_generate_pdf("file:///" + html_filename, Path(filename).stem + ".pdf"))

    os.remove(html_filename)
    os.remove(CSS_FILENAME)
    shutil.rmtree("node_modules")

def _generate_style_css() -> None:
    res = os.system(f'github-markdown-css --theme=dark_dimmed >> {CSS_FILENAME}')
    if res != 0:
        raise Exception(f"{CSS_FILENAME} could not be created")

def _generate_html(filename) -> str:
    html_file = Path(filename).stem + ".html"

    md = MarkdownIt("commonmark", {"html": True}) \
                    .use(front_matter_plugin) \
                    .use(footnote_plugin) \
                    .enable('table')
    
    with open(filename, "r") as f:
        raw_html = md.render(f.read())
    
    prefix = HTML_PREFIX.replace("F1L3N4M3H3R3", Path(filename).name) \
                        .replace("STYLE_F1L3_H3R3", CSS_FILENAME)

    postfix = HTML_POSTFIX

    with open(html_file, "w+") as f:
        f.write(prefix + raw_html + postfix)
    
    return str(Path(html_file).resolve())

async def _generate_pdf(url, pdf_path):
    browser = await launch()
    page = await browser.newPage()

    await page.goto(url)

    # await page.screenshot({"path": "sample.png"})
    
    height = await _get_page_height(page)
    await page.pdf({"path": pdf_path, "printBackground": True, "height": f"{height}px", "pageRanges": "1"})

    print(f"Generated file {Path(pdf_path).name}")

    await browser.close()

async def _get_page_height(page: Page) -> float:
    """
    Code from here:
    https://stackoverflow.com/a/70355152/15436169
    """

    return await page.evaluate('''() => {
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

HTML_POSTFIX = """
</body>
</html>
"""

if __name__ == "__main__":
    main()
