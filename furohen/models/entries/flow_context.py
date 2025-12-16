from .node import Node


class FlowContext:
    def __init__(self, entry: Node, exit: list[Node], *, is_while=False) -> None:
        self.entry: Node = entry
        self.exit: list[Node] = exit
        self.is_while: bool = is_while
