from typing import Callable

from pycparser.c_ast import Assignment, Compound, Decl, FuncCall, If
from pycparser.c_ast import Node as ASTNode
from pycparser.c_ast import Return, While

from furohen.convert import to_str
from furohen.models import FlowContext, Node

stmt_format_mapping = dict()


def build_stmt(stmt) -> FlowContext | None:
    fmt = type(stmt)
    if fmt not in stmt_format_mapping:
        return None
    return stmt_format_mapping[fmt](stmt)


def register_stmt(fmt: type):
    def decorator(func: Callable):
        stmt_format_mapping[fmt] = func
        return func

    return decorator


# def _build_stmt(stmt) -> FlowContext | None:
#     if isinstance(stmt, list):
#         return build_block(stmt)
#     if isinstance(stmt, (Decl, Assignment, FuncCall)):
#         return build_simple(stmt)
#     if isinstance(stmt, If):
#         return build_if(stmt)
#     if isinstance(stmt, Compound):
#         return build_block(stmt.block_items)
#     if isinstance(stmt, Return):
#         node = Node(text=to_str(stmt), shape="doublecircle")
#         return FlowContext(node, [])
#     if isinstance(stmt, While):
#         cond_node = Node(text=to_str(stmt.cond), shape="diamond")

#         body_ctx = build_stmt(stmt.stmt)
#         if body_ctx:
#             cond_node.add_node(body_ctx.entry, "Yes")
#             for e in body_ctx.exit:
#                 e.add_node(cond_node)

#         # No 分支直接接到下一個節點
#         return FlowContext(cond_node, [cond_node])
#     return None


@register_stmt(list)
def build_block(body: list[ASTNode]) -> FlowContext | None:
    prev: FlowContext | None = None
    entry: Node | None = None

    for item in body:
        ctx = build_stmt(item)
        if ctx is None:
            continue

        if entry is None:
            entry = ctx.entry

        if prev:
            exits = prev.exit if isinstance(prev.exit, list) else [prev.exit]
            for e in exits:
                e.add_node(ctx.entry)

        prev = ctx

    return FlowContext(entry, prev.exit) if entry and prev else None


@register_stmt(Assignment)
@register_stmt(Decl)
@register_stmt(FuncCall)
def build_simple(stmt: Assignment | Decl | FuncCall) -> FlowContext:
    n = Node(text=to_str(stmt), shape="box")
    return FlowContext(n, [n])


@register_stmt(Compound)
def build_stmt_compound(stmt: Compound) -> FlowContext | None:
    return build_block(stmt.block_items)


@register_stmt(If)
def build_if(stmt: If) -> FlowContext:
    cond_node = Node(text=to_str(stmt.cond), shape="diamond")

    exits: list[Node] = []

    # yes 分支
    true_ctx = build_stmt(stmt.iftrue)
    if true_ctx:
        cond_node.add_node(true_ctx.entry, "Yes")
        if isinstance(true_ctx.exit, list):
            exits.extend(true_ctx.exit)
        else:
            exits.append(true_ctx.exit)
    else:
        exits.append(cond_node)

    # no 分支
    false_ctx = build_stmt(stmt.iffalse) if stmt.iffalse else None
    if false_ctx:
        cond_node.add_node(false_ctx.entry, "No")
        if isinstance(false_ctx.exit, list):
            exits.extend(false_ctx.exit)
        else:
            exits.append(false_ctx.exit)
    else:
        exits.append(cond_node)

    return FlowContext(cond_node, exits)


@register_stmt(Return)
def build_return(stmt: Return) -> FlowContext:
    node = Node(text=to_str(stmt), shape="doublecircle")
    return FlowContext(node, [])

