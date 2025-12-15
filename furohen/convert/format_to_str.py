from typing import Any, Optional

from pycparser.c_ast import (
    ID,
    Assignment,
    BinaryOp,
    Constant,
    Decl,
    FuncCall,
    If,
    Return,
    While,
)

format_dict = dict()


def register_format(node_type):
    def decorator(func):
        format_dict[node_type] = func
        return func

    return decorator


@register_format(ID)
def id_to_str(node: ID) -> Optional[str]:
    return node.name


# x = 10; -> 10をxになる
@register_format(Assignment)
def assignment_to_str(assignment: Assignment) -> Optional[str]:
    op = assignment.op
    name = assignment.lvalue.name
    value = assignment.rvalue.value
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
    name = decl.name
    if decl.init is None:
        return f"{name}を宣言"
    value = decl.init.value
    return f"{name}を{value}になる"


# FuncCall -> printf("Hello, World!"); -> Hello, World!を出力
@register_format(FuncCall)
def funccall_to_str(funccall: FuncCall) -> Optional[str]:
    name = funccall.name.name
    if name == "printf":
        format_str = funccall.args.exprs[0].value
        return f"{format_str}を出力"
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
    if ret.expr is None:
        return "終了"
    value = ret.expr.value
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
