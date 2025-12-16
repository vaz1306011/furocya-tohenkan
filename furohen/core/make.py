import logging

from pycparser.c_ast import FuncDef

from furohen.models import Node, Shape

from .build import build_block

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def make(funcs: list[FuncDef]) -> list[Node]:
    head_nodes: list[Node] = []

    for func in funcs:
        # 建立函式入口節點
        if func.decl.name == "main":
            start = Node("開始", shape=Shape.DOUBLECIRCLE)
        else:
            start = Node(f"{func.decl.name}を定義", shape=Shape.OVAL)

        # 轉換函式本體
        body = func.body.block_items
        logger.debug(body)
        ctx = build_block(body)

        if ctx:
            # 開始 → 函式第一個流程節點
            start.add_node(ctx.entry)

            # 建立結束節點
            end = Node("終了", shape=Shape.DOUBLECIRCLE)
            for e in ctx.exit:
                e.add_node(end)
        else:
            # 空函式直接接到結束
            end = Node("終了", shape=Shape.DOUBLECIRCLE)
            start.add_node(end)

        head_nodes.append(start)

    return head_nodes
