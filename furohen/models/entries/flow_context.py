from typing import Optional

from .node import Node


class FlowContext:
    def __init__(self, entry: Node, exit: Optional[Node] = None):
        self.entry: Node = entry
        self.exit: Optional[Node] = exit
