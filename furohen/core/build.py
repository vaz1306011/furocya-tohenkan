from typing import Callable

from pycparser.c_ast import Assignment, Break, Case, Compound, Decl, Default, FuncCall, If, Switch
from pycparser.c_ast import Node as ASTNode
from pycparser.c_ast import Return, While

from furohen.convert import to_str
from furohen.models import FlowContext, Node, Shape

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
            exits = prev.exit
            for e in exits:
                if prev.is_while:
                    e.add_node(ctx.entry, "No", constraint="false")
                else:
                    e.add_node(ctx.entry)

        prev = ctx

    return FlowContext(entry, prev.exit) if entry and prev else None


@register_stmt(Assignment)
@register_stmt(Decl)
@register_stmt(FuncCall)
def build_simple(stmt: Assignment | Decl | FuncCall) -> FlowContext:
    n = Node(text=to_str(stmt))
    return FlowContext(n, [n])


@register_stmt(Compound)
def build_stmt_compound(stmt: Compound) -> FlowContext | None:
    return build_block(stmt.block_items)


def build_case_block(stmts: list[ASTNode]) -> tuple[Node | None, list[Node], bool]:
    prev: FlowContext | None = None
    entry: Node | None = None

    for item in stmts or []:
        if isinstance(item, Break):
            break_node = Node(text="break")
            if entry is None:
                entry = break_node
            if prev:
                for e in prev.exit:
                    e.add_node(break_node)
            return entry, [break_node], True

        ctx = build_stmt(item)
        if ctx is None:
            continue

        if entry is None:
            entry = ctx.entry

        if prev:
            exits = prev.exit
            for e in exits:
                if prev.is_while:
                    e.add_node(ctx.entry, "No", constraint="false")
                else:
                    e.add_node(ctx.entry)

        prev = ctx

    if prev:
        return entry, prev.exit, False

    return None, [], False


@register_stmt(Switch)
def build_switch(stmt: Switch) -> FlowContext:
    cond_node = Node(text=f"switch {to_str(stmt.cond)}", shape=Shape.DIAMOND)
    switch_end = Node("switch終了", shape=Shape.OVAL)

    items = []
    if isinstance(stmt.stmt, Compound):
        items = stmt.stmt.block_items or []
    else:
        items = [stmt.stmt]

    cases: list[tuple[str, Node, list[Node], bool]] = []

    for item in items:
        if isinstance(item, Case):
            label = f"case {to_str(item.expr)}"
            entry, exits, has_break = build_case_block(item.stmts or [])
            if entry is None:
                entry = Node(text="空のcase")
            cases.append((label, entry, exits, has_break))
        elif isinstance(item, Default):
            label = "default"
            entry, exits, has_break = build_case_block(item.stmts or [])
            if entry is None:
                entry = Node(text="空のdefault")
            cases.append((label, entry, exits, has_break))

    if not cases:
        cond_node.add_node(switch_end)
        return FlowContext(cond_node, [switch_end])

    for label, entry, _, _ in cases:
        cond_node.add_node(entry, label)

    for i, (_, entry, exits, has_break) in enumerate(cases):
        if not exits:
            exits = [entry]
        if has_break or i == len(cases) - 1:
            for e in exits:
                e.add_node(switch_end)
        else:
            next_entry = cases[i + 1][1]
            for e in exits:
                e.add_node(next_entry)

    return FlowContext(cond_node, [switch_end])


@register_stmt(If)
def build_if(stmt: If) -> FlowContext:
    cond_node = Node(text=to_str(stmt.cond), shape=Shape.DIAMOND)

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
    node = Node(text=to_str(stmt), shape=Shape.OVAL)
    return FlowContext(node, [])


@register_stmt(While)
def build_while(stmt: While) -> FlowContext:
    cond_node = Node(text=to_str(stmt.cond), shape=Shape.DIAMOND)

    body_ctx = build_stmt(stmt.stmt)

    if not body_ctx:
        return FlowContext(cond_node, [cond_node], is_while=True)

    cond_node.add_node(body_ctx.entry, "Yes")

    for e in body_ctx.exit:
        e.add_node(cond_node)

    return FlowContext(cond_node, [cond_node], is_while=True)
