import locale
import logging
import subprocess

from graphviz import Digraph

from furohen.models import Node

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def render(node: Node | list[Node], filename="flowchart", view=False) -> None:
    g = Digraph("flowchart", engine="dot")
    g.attr(
        rankdir="TB",
        nodesep="0.8",
        ranksep="1.0",
        splines="ortho",
        fontname="Microsoft JhengHei",
    )
    g.attr("node", fontname="Microsoft JhengHei")
    g.attr("edge", fontname="Microsoft JhengHei")

    stack = node if isinstance(node, list) else [node]
    visited: set[str] = set()

    while stack:
        node = stack.pop()

        if node.id in visited:
            continue
        visited.add(node.id)

        g.node(node.id, node.text, shape=node.shape.value)

        for line in node.lines:
            g.edge(node.id, line.node.id, xlabel=line.text, constraint=line.constraint)
            stack.append(line.node)

    g.render(filename, format="pdf", view=view)
