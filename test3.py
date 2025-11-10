from pycparser import c_parser

code = r"""
int main(void) {
  printf("%cは文字です。\n", 'A');
  printf("%dは整数です。\n", 123);
  printf("%fは小数です。\n", 10.5);

  return 0;
}
"""

fc = c_parser.CParser()
ast = fc.parse(code)
ast.show()
