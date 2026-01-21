import logging
from typing import Callable, Optional

from pycparser.c_ast import ID, Assignment, BinaryOp, Constant, Decl, FuncCall, If
from pycparser.c_ast import Node as ASTNode
from pycparser.c_ast import Return, UnaryOp, While

from furohen.exceptions import UnsupportedASTTypeException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

node_format_mapping = dict()


def to_str(node: ASTNode) -> str:
    node_type = type(node)
    if not node_type in node_format_mapping:
        raise UnsupportedASTTypeException(node_type)
    return node_format_mapping[node_type](node)


def register_format(node_type: type):
    def decorator(func: Callable):
        node_format_mapping[node_type] = func
        return func

    return decorator


@register_format(ID)
def id_to_str(node: ID) -> Optional[str]:
    return node.name


# x = 10; -> 10をxになる
@register_format(Assignment)
def assignment_to_str(assignment: Assignment) -> Optional[str]:
    from furohen.convert.convert import to_str

    op = assignment.op
    name = assignment.lvalue.name
    value = to_str(assignment.rvalue)
    if op == "=":
        return f"{name}を{value}になる"
    return None


@register_format(BinaryOp)
def binaryop_to_str(binop: BinaryOp) -> Optional[str]:
    from furohen.convert.convert import to_str

    left = to_str(binop.left)
    right = to_str(binop.right)
    return f"{left} {binop.op} {right}"


@register_format(Constant)
def constant_to_str(constant: Constant) -> Optional[str]:
    return constant.value


# int x; -> xを宣言
# int x = 10; -> xを10になる
@register_format(Decl)
def decl_to_str(decl: Decl) -> Optional[str]:
    from furohen.convert.convert import to_str

    name = decl.name
    if decl.init is None:
        return f"{name}を宣言"
    value = to_str(decl.init)
    return f"{name}を{value}になる"


# FuncCall -> printf("Hello, World!"); -> Hello, World!を出力
@register_format(FuncCall)
def funccall_to_str(funccall: FuncCall) -> Optional[str]:
    name = funccall.name.name
    if name == "printf":
        args = funccall.args.exprs if funccall.args else []
        format_str = args[0].value if args else '""'
        fmt = format_str
        if len(fmt) >= 2 and fmt[0] == '"' and fmt[-1] == '"':
            fmt = fmt[1:-1]
        out = []
        arg_index = 1
        i = 0
        while i < len(fmt):
            if fmt[i] != "%":
                out.append(fmt[i])
                i += 1
                continue
            if i + 1 < len(fmt) and fmt[i + 1] == "%":
                out.append("%")
                i += 2
                continue
            j = i + 1
            while j < len(fmt) and fmt[j] in "0123456789.-+ #hlLzjt":
                j += 1
            if j < len(fmt):
                j += 1
            if arg_index < len(args):
                out.append(to_str(args[arg_index]))
                arg_index += 1
            i = j
        return f"\"{''.join(out)}\"を出力"
    elif name in ("scanf", "scanf_s"):
        args = funccall.args.exprs if funccall.args else []
        names: list[str] = []
        for arg in args[1:]:
            if isinstance(arg, ID):
                names.append(arg.name)
                continue
            if isinstance(arg, UnaryOp) and arg.op == "&" and hasattr(arg.expr, "name"):
                names.append(arg.expr.name)
        if names:
            return f"{'、'.join(names)}を入力"
        format_str = funccall.args.exprs[0].value
        return f"{format_str}を入力"
    else:
        return f"{name}を呼び出す"


# if(x == 10) -> もしxが10と等しい場合
@register_format(If)
def if_to_str(if_stmt: If) -> Optional[str]:
    from furohen.convert.convert import to_str

    cond = if_stmt.cond
    tail = {
        "==": "と等しい場合",
        "!=": "と等しくない場合",
        "<": "より小さい場合",
        "<=": "以下の場合",
        ">": "より大きい場合",
        ">=": "以上の場合",
    }
    return f"もし{to_str(cond.left)}が{to_str(cond.right)}{tail[cond.op]}"


@register_format(Return)
def return_to_str(ret: Return) -> Optional[str]:
    from furohen.convert.convert import to_str

    if ret.expr is None:
        return "終了"
    value = to_str(ret.expr)
    return f"{value}を返す"


@register_format(While)
def while_to_str(while_stmt: While) -> Optional[str]:
    op = while_stmt.cond.op
    left = while_stmt.cond.left
    right = while_stmt.cond.right
    tail = {
        "==": "と等しい間",
        "!=": "と等しくない間",
        "<": "より小さい間",
        "<=": "以下の間",
        ">": "より大きい間",
        ">=": "以上の間",
    }
    if op in tail:
        condition_str = f"while {left.name}が{right.value}{tail[op]}"
    else:
        raise NotImplementedError(f"Unsupported operator: {op}")

    return condition_str
