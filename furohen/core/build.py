from typing import Callable

from pycparser.c_ast import (
    Assignment,
    Break,
    Case,
    Constant,
    Compound,
    Decl,
    Default,
    DoWhile,
    For,
    FuncCall,
    If,
)
from pycparser.c_ast import Node as ASTNode
from pycparser.c_ast import Continue, Return, Switch, While

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
    break_exit: list[Node] = []
    break_labels: dict[Node, str] = {}
    continue_exit: list[Node] = []
    continue_labels: dict[Node, str] = {}
    no_exit: list[Node] = []

    for item in body:
        if isinstance(item, Break):
            break_node = None
            if prev:
                if entry is None:
                    entry = prev.entry
                break_exit.extend(prev.exit)
            else:
                break_node = Node(text="break")
                if entry is None:
                    entry = break_node
                break_exit.append(break_node)
            if entry is None:
                entry = break_node
            if entry is None:
                return None
            return FlowContext(
                entry,
                [],
                break_exit=break_exit,
                break_labels=break_labels,
                continue_exit=continue_exit,
                continue_labels=continue_labels,
                no_exit=[],
            )

        ctx = build_stmt(item)
        if ctx is None:
            continue

        if entry is None:
            entry = ctx.entry
        if ctx.break_exit and not ctx.is_while:
            break_exit.extend(ctx.break_exit)
            break_labels.update(ctx.break_labels)
        if ctx.continue_exit:
            continue_exit.extend(ctx.continue_exit)
            continue_labels.update(ctx.continue_labels)

        if prev:
            exits = prev.exit
            for e in exits:
                if prev.is_while:
                    e.add_node(ctx.entry, "No")
                elif e in prev.no_exit:
                    e.add_node(ctx.entry, "No")
                else:
                    e.add_node(ctx.entry)
            if prev.is_while and prev.break_exit:
                for e in prev.break_exit:
                    label = prev.break_labels.get(e)
                    if label:
                        e.add_node(ctx.entry, label)
                    else:
                        e.add_node(ctx.entry)

        prev = ctx
        no_exit = ctx.no_exit

    if not entry or not prev:
        return None
    return FlowContext(
        entry,
        prev.exit,
        break_exit=break_exit,
        break_labels=break_labels,
        continue_exit=continue_exit,
        continue_labels=continue_labels,
        no_exit=no_exit,
    )


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
                    e.add_node(ctx.entry, "No")
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
    break_exit: list[Node] = []
    break_labels: dict[Node, str] = {}
    continue_exit: list[Node] = []
    continue_labels: dict[Node, str] = {}
    no_exit: list[Node] = []

    def handle_branch(branch, label: str, *, is_false: bool = False) -> None:
        if isinstance(branch, Break):
            break_exit.append(cond_node)
            break_labels[cond_node] = label
            return
        ctx = build_stmt(branch) if branch is not None else None
        if ctx:
            cond_node.add_node(ctx.entry, label)
            exits.extend(ctx.exit if isinstance(ctx.exit, list) else [ctx.exit])
            if ctx.break_exit:
                break_exit.extend(ctx.break_exit)
                break_labels.update(ctx.break_labels)
            if ctx.continue_exit:
                continue_exit.extend(ctx.continue_exit)
                continue_labels.update(ctx.continue_labels)
        else:
            exits.append(cond_node)
            if is_false:
                no_exit.append(cond_node)

    # yes / no 分支
    handle_branch(stmt.iftrue, "Yes")
    handle_branch(stmt.iffalse, "No", is_false=True)

    return FlowContext(
        cond_node,
        exits,
        break_exit=break_exit,
        break_labels=break_labels,
        continue_exit=continue_exit,
        continue_labels=continue_labels,
        no_exit=no_exit,
    )


@register_stmt(Return)
def build_return(stmt: Return) -> FlowContext:
    node = Node(text=to_str(stmt), shape=Shape.OVAL)
    return FlowContext(node, [])


@register_stmt(While)
def build_while(stmt: While) -> FlowContext:
    is_infinite = isinstance(stmt.cond, Constant) and stmt.cond.value == "1"
    cond_node = Node(text=to_str(stmt.cond), shape=Shape.DIAMOND)

    body_ctx = build_stmt(stmt.stmt)

    if not body_ctx:
        return FlowContext(cond_node, [cond_node], is_while=True)

    cond_node.add_node(body_ctx.entry, "Yes")

    for e in body_ctx.exit:
        if not is_infinite and e in body_ctx.no_exit:
            e.add_node(cond_node, "No")
        else:
            e.add_node(cond_node)
    for e in body_ctx.continue_exit:
        label = body_ctx.continue_labels.get(e)
        if label and not is_infinite:
            e.add_node(cond_node, label)
        else:
            e.add_node(cond_node)

    exit_nodes = [] if is_infinite else [cond_node]
    return FlowContext(
        cond_node,
        exit_nodes,
        is_while=True,
        break_exit=body_ctx.break_exit,
        break_labels=body_ctx.break_labels,
    )


@register_stmt(DoWhile)
def build_do_while(stmt: DoWhile) -> FlowContext:
    cond_node = Node(text=to_str(stmt.cond), shape=Shape.DIAMOND)

    body_ctx = build_stmt(stmt.stmt)

    if not body_ctx:
        return FlowContext(cond_node, [cond_node], is_while=True)

    for e in body_ctx.exit:
        if e in body_ctx.no_exit:
            e.add_node(cond_node, "No")
        else:
            e.add_node(cond_node)
    for e in body_ctx.continue_exit:
        label = body_ctx.continue_labels.get(e)
        if label:
            e.add_node(cond_node, label)
        else:
            e.add_node(cond_node)

    cond_node.add_node(body_ctx.entry, "Yes")

    return FlowContext(
        body_ctx.entry,
        [cond_node],
        is_while=True,
        break_exit=body_ctx.break_exit,
        break_labels=body_ctx.break_labels,
    )


@register_stmt(For)
def build_for(stmt: For) -> FlowContext:
    init_node = Node(text=to_str(stmt.init)) if stmt.init else None
    cond_text = to_str(stmt.cond) if stmt.cond else "true"
    cond_node = Node(text=cond_text, shape=Shape.DIAMOND)
    next_node = Node(text=to_str(stmt.next)) if stmt.next else None

    body_ctx = build_stmt(stmt.stmt)

    entry = cond_node
    if init_node:
        init_node.add_node(cond_node)
        entry = init_node

    def attach_loop_back(target: Node, ctx: FlowContext) -> None:
        for e in ctx.exit:
            if e in ctx.no_exit:
                e.add_node(target, "No")
            else:
                e.add_node(target)
        for e in ctx.continue_exit:
            label = ctx.continue_labels.get(e)
            if label:
                e.add_node(target, label)
            else:
                e.add_node(target)

    if body_ctx:
        cond_node.add_node(body_ctx.entry, "Yes")
        if next_node:
            attach_loop_back(next_node, body_ctx)
            next_node.add_node(cond_node)
        else:
            attach_loop_back(cond_node, body_ctx)
    else:
        empty_body = Node("空の処理")
        cond_node.add_node(empty_body, "Yes")
        if next_node:
            empty_body.add_node(next_node)
            next_node.add_node(cond_node)
        else:
            empty_body.add_node(cond_node)

    loop_break_exit = body_ctx.break_exit if body_ctx else []
    loop_break_labels = body_ctx.break_labels if body_ctx else {}
    return FlowContext(
        entry,
        [cond_node],
        is_while=True,
        break_exit=loop_break_exit,
        break_labels=loop_break_labels,
    )


@register_stmt(Break)
def build_break(stmt: Break) -> FlowContext:
    break_node = Node(text="break")
    return FlowContext(break_node, [], break_exit=[break_node])


@register_stmt(Continue)
def build_continue(stmt: Continue) -> FlowContext:
    continue_node = Node(text="continue")
    return FlowContext(continue_node, [], continue_exit=[continue_node])
