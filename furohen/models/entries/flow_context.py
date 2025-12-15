from .node import Node


class FlowContext:
    def __init__(self, entry: Node, exit: list[Node]) -> None:
        self.entry: Node = entry
        self.exit: list[Node] = exit
