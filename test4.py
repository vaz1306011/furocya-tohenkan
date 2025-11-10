from pycparser import c_parser

code = r"""
int main() {
    int x = 3;
    if (x > 0) {
        x = 1;
    } else {
        x = -1;
    }
    return x;
}
"""

parser = c_parser.CParser()
ast = parser.parse(code)

ast.show()
