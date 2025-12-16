from ..enums.shape import Shape


class Node:
    def __init__(self, text: str, shape: Shape = Shape.BOX) -> None:
        self.text: str = text
        self.shape: Shape = shape
        self.lines: list[Line] = []

    def __str__(self) -> str:
        return f"Node({self.text}[{self.shape}], len(lines)={len(self.lines) if self.lines else 0})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def id(self) -> str:
        return str(id(self))

    def add_node(self, node: "Node", text: str = "", *, constraint="true") -> None:
        self.lines.append(Line(node, text, constraint=constraint))


class Line:
    def __init__(self, node: Node, text: str = "", constraint="true") -> None:
        self.text: str = text
        self.node: "Node" = node
        self.constraint: str = constraint
