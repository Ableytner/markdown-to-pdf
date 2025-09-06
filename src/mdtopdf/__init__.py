"""
A library for converting any Markdown document to PDF, utilizing Githubs' styling.

To get started, import the ```convert``` method.
"""

import sys

from .convert import convert

def main():
    """The method called when using this package from the console"""

    if len(sys.argv) < 2:
        # pylint: disable-next=broad-exception-raised
        raise Exception("No filename provided, example usage: python3 -m mdtopdf myfile.md")

    source_file = sys.argv[1]

    convert(source_file)

__exports__ = [
    convert
]
