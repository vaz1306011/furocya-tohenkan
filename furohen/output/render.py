import logging

from graphviz import Digraph

from furohen.models import Node

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def render(node: Node, filename="flowchart", view=False) -> None:
    g = Digraph("flowchart")

    stack = [node]
    while True:
        node = stack.pop()
        g.node(node.id, node.text, shape=node.shape)

        if not node.lines:
            if stack:
                continue
            break

        for line in node.lines:
            g.edge(node.id, line.node.id, label=line.text)
            stack.append(line.node)

    g.node("end", "結束", shape="doublecircle")
    g.edge(node.id, "end")

    g.render(filename, format="pdf", view=view)
