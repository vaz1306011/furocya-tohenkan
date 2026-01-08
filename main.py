import logging
from pathlib import Path

from furohen.core import make
from furohen.output import render
from furohen.utils import read_code, read_file, setup_logging

setup_logging()
logger = logging.getLogger(__name__)

FILE = Path("./test_data/if.c")

if __name__ == "__main__":
    code = read_file(FILE)
    if not code:
        exit(1)

    funcs = read_code(code)

    nodes = make(funcs)

    render(nodes[0], FILE.stem + ".gv", view=True)
