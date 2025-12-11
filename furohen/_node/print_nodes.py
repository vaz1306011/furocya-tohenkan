import logging

from furohen.models import Node

logger = logging.getLogger(__name__)


def nprint(node: Node) -> None:
    while True:
        print(str(node))
        if not node.lines:
            break
        line = node.lines[0]
        node = line.node
