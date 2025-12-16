import locale
import logging
import subprocess

from graphviz import Digraph

from furohen.models import Node

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def render(node: Node, filename="flowchart", view=False) -> None:
    def render_pdf(g: Digraph, filename: str, view: bool = False):
        enc = locale.getpreferredencoding()
        dot_file = filename + ".dot"
        pdf_file = filename + ".pdf"

        with open(dot_file, "w", encoding=enc) as f:
            f.write(g.source)

        subprocess.run(["dot", "-Tpdf", dot_file, "-o", pdf_file])

        if view:
            import os

            (
                os.startfile(pdf_file)
                if os.name == "nt"
                else subprocess.run(["open", pdf_file])
            )

        return pdf_file

    g = Digraph("flowchart", engine="dot")
    g.attr(
        rankdir="TB",
        nodesep="0.8",
        ranksep="1.0",
        splines="ortho",
    )

    stack = [node]
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

    render_pdf(g, filename, view)
