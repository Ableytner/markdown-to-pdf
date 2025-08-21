"""The main module, used when calling from the console and for dev testing"""

import sys
from markdowntopdf import convert

if __name__ == "__main__":
    if len(sys.argv) == 0:
        # pylint: disable-next=broad-exception-raised
        raise Exception("No filename provided, example usage: python3 -m markdown-2-pdf myfile.md")

    source_file = sys.argv[1]

    convert(source_file)
