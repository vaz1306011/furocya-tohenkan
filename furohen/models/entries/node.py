class Node:
    def __init__(self, text: str, shape: str = "box") -> None:
        self.text: str = text
        self.shape: str = shape
        self.lines: list[Line] = []

    def __str__(self) -> str:
        return f"Node({self.text}[{self.shape}], len(lines)={len(self.lines) if self.lines else 0})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def id(self) -> str:
        return str(id(self))

    def add_node(self, node: "Node", text: str = "") -> None:
        self.lines.append(Line(node, text))


class Line:
    def __init__(self, node: Node, text: str = "") -> None:
        self.text: str = text
        self.node: "Node" = node
