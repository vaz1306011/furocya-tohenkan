from .node import Node


class FlowContext:
    def __init__(
        self,
        entry: Node,
        exit: list[Node],
        *,
        is_while=False,
        break_exit: list[Node] | None = None,
        break_labels: dict[Node, str] | None = None,
        continue_exit: list[Node] | None = None,
        continue_labels: dict[Node, str] | None = None,
        no_exit: list[Node] | None = None,
    ) -> None:
        self.entry: Node = entry
        self.exit: list[Node] = exit
        self.is_while: bool = is_while
        self.break_exit: list[Node] = break_exit or []
        self.break_labels: dict[Node, str] = break_labels or {}
        self.continue_exit: list[Node] = continue_exit or []
        self.continue_labels: dict[Node, str] = continue_labels or {}
        self.no_exit: list[Node] = no_exit or []
