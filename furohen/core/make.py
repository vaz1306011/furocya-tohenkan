import logging
from pprint import pprint

from graphviz import Digraph
from pycparser.c_ast import Decl, FileAST, FuncDef
from pycparser.c_parser import CParser

from furohen.convert import to_node
from furohen.models import Node

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def make(funcs: list[FuncDef]) -> list[Node]:
    head_nodes: list[Node] = []
    for func in funcs:
        name = func.decl.name
        if name == "main":
            head_nodes.append(Node("開始", shape="doublecircle"))
        else:
            head_nodes.append(Node(f"{name}を定義", shape="oval"))

        block_items = func.body.block_items
        last_node = head_nodes[-1]
        for item in block_items:
            node = to_node(item)
            last_node.add_node(node)
            last_node = node

    return head_nodes
