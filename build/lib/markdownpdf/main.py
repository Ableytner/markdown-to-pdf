import asyncio
import sys
import os
from pathlib import Path

from pyppeteer import launch
from pyppeteer.page import Page

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        raise Exception("No filename provided")

    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    if not os.path.isabs(filename):
        filename = os.path.join(os.getcwd(), filename)

    asyncio.get_event_loop().run_until_complete(_generate_pdf("file:///" + filename, Path(filename).stem + ".pdf"))

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

if __name__ == "__main__":
    main()
