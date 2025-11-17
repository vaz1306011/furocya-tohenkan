import pprint

import pycparser
import pycparser.c_ast
from pycparser import c_parser

from furohen.utils.file import read_file

code = read_file("./test_data/test_data.c")
parser = c_parser.CParser()
ast: pycparser.c_ast.FileAST = parser.parse(code)

pprint.pprint(ast.children())
