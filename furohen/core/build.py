from pycparser.c_ast import Assignment, Compound, Decl, FuncCall, If, Return, While

from furohen.convert import to_str
from furohen.models import FlowContext, Node


def build_if(stmt) -> FlowContext:
    cond_node = Node(text=to_str(stmt.cond), shape="diamond")

    true_ctx = build_stmt(stmt.iftrue)
    if true_ctx:
        cond_node.add_node(true_ctx.entry, "Yes")

    false_ctx = None
    if stmt.iffalse:
        false_ctx = build_stmt(stmt.iffalse)
        false_ctx and cond_node.add_node(false_ctx.entry, "No")

    merge = Node(text="", shape="circle")

    if true_ctx and true_ctx.exit:
        true_ctx.exit.add_node(merge)
    if false_ctx and false_ctx.exit:
        false_ctx.exit.add_node(merge)
    else:
        cond_node.add_node(merge, "No")

    return FlowContext(cond_node, merge)


def build_block(stmts) -> FlowContext | None:
    prev = None
    entry = None

    for s in stmts:
        ctx = build_stmt(s)
        if ctx is None:
            continue
        if entry is None:
            entry = ctx.entry
        if prev and prev.exit:
            prev.exit.add_node(ctx.entry)
        prev = ctx

    return FlowContext(entry, prev.exit) if entry and prev else None


def build_simple(stmt) -> FlowContext:
    n = Node(text=to_str(stmt), shape="box")
    return FlowContext(n, n)


def build_stmt(stmt) -> FlowContext | None:
    if isinstance(stmt, (Decl, Assignment, FuncCall, Return)):
        return build_simple(stmt)
    if isinstance(stmt, If):
        return build_if(stmt)
    if isinstance(stmt, Compound):
        return build_block(stmt.block_items)
    return None
