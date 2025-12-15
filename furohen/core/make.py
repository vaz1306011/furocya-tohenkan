import logging
from pprint import pprint

from graphviz import Digraph
from pycparser.c_ast import Decl, FileAST, FuncDef
from pycparser.c_parser import CParser

from furohen.convert import to_node
from furohen.models import Node

from .build import build_block

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def make(funcs: list[FuncDef]) -> list[Node]:
    head_nodes: list[Node] = []

    for func in funcs:
        # 建立函式入口節點
        if func.decl.name == "main":
            start = Node("開始", shape="doublecircle")
        else:
            start = Node(f"{func.decl.name}を定義", shape="oval")

        # 轉換函式本體
        body = func.body.block_items
        ctx = build_block(body)

        if ctx:
            # 開始 → 函式第一個流程節點
            start.add_node(ctx.entry)

            # 建立結束節點
            end = Node("終了", shape="doublecircle")
            ctx.exit and ctx.exit.add_node(end)
        else:
            # 空函式直接接到結束
            end = Node("終了", shape="doublecircle")
            start.add_node(end)

        head_nodes.append(start)

    return head_nodes
